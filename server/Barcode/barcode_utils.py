# barcode_utils.py

import cv2
from pyzbar.pyzbar import decode
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri: str = os.getenv("MONGO_ATLAS_URI")

def get_mongo_connection(uri=uri, db_name="food-stat", collection_name="food_items"):
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]

from bson import ObjectId

def check_barcode_in_mongo(barcode_data, collection):
    if not barcode_data:
        print("[ERROR] No barcode data to match.")
        return None

    result = collection.find_one({"barcode": barcode_data})
    if result:
        print("[✅] Match found in database!")
        result['_id'] = str(result['_id'])  # 👈 Convert ObjectId to string
        return result
    else:
        print("[❌] No match found in the database.")
        return None


def analyze_barcode_from_base64(base64_data):
    import base64
    import io
    from PIL import Image

    try:
        image_data = base64.b64decode(base64_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        barcodes = decode(frame)
        results = []

        if not barcodes:
            print("[❌] No barcodes found in image.")
        else:
            print(f"[🔍] Found {len(barcodes)} barcode(s)")

        collection = get_mongo_connection()

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            print(f"[✅] Decoded: {barcode_type} | {barcode_data}")

            try:
                product = check_barcode_in_mongo(barcode_data, collection)
            except Exception as e:
                print(f"[⚠️] Error querying Mongo: {e}")
                product = None

            results.append({
                "type": barcode_type,
                "data": barcode_data,
                "product": product
            })
            print(results)

        return results

    except Exception as e:
        print(f"[❌] Barcode analysis failed: {e}")
        return []
