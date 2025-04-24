import cv2
from pyzbar.pyzbar import decode
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri: str = os.getenv("MONGO_ATLAS_URI")

def analyze_barcode_from_frame(frame):
    barcodes = decode(frame)
    if not barcodes:
        print("[INFO] No barcode found.")
        return

    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        points = barcode.polygon

        # Draw rectangle around the barcode
        pts = [(point.x, point.y) for point in points]
        cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Show barcode data
        cv2.putText(frame, f'{barcode_type}: {data}', (pts[0][0], pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        print(f'[INFO] Detected {barcode_type}: {data}')

    cv2.imshow("Captured Frame Analysis", frame)
    cv2.waitKey(3000)
    cv2.destroyWindow("Captured Frame Analysis")

def capture_and_analyze(camera_index):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[ERROR] Unable to access camera {camera_index}")
        return

    print(f"Camera {camera_index} started. Press 'c' to capture and analyze, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        cv2.imshow("Live Feed", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            print("[INFO] Captured frame for barcode analysis.")
            analyze_barcode_from_frame(frame)

    cap.release()
    cv2.destroyAllWindows()


def check_barcode_in_mongo(barcode_data, collection):
    if not barcode_data:
        print("[ERROR] No barcode data to match.")
        return

    result = collection.find_one({"barcode": barcode_data})
    if result:
        print("[✅] Match found in database!")
        print("Product Details:", result)
    else:
        print("[❌] No match found in the database.")


def get_mongo_connection(uri=uri, db_name="food-stat", collection_name="food_items"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]


def example():
    try:
        camera_index = int(input("Enter camera source index (default is 0): ") or 0)
    except ValueError:
        camera_index = 0

    capture_and_analyze(camera_index)
