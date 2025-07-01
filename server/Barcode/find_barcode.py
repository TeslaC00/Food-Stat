import cv2
from pyzbar.pyzbar import decode
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
uri: str = os.getenv("MONGO_ATLAS_URI")

def get_mongo_connection(uri=uri, db_name="food-stat", collection_name="food_items"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]

def analyze_barcode_from_image(image_path):
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return None

    image = cv2.imread(image_path)
    barcodes = decode(image)

    if not barcodes:
        print("[INFO] No barcode found in the image.")
        return None

    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        print(f"[INFO] Found {barcode.type} barcode with data: {data}")
        return data

    return None

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

if __name__ == "__main__":
    image_path = "barcode.jpg"
    barcode_data = analyze_barcode_from_image(image_path)

    # Connect to MongoDB
    collection = get_mongo_connection()

    # Search for barcode match
    check_barcode_in_mongo(barcode_data, collection)
