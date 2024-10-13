from flask import Flask
from database import db
from bson import json_util

app = Flask(__name__)
collection = db["food_items"]


@app.route("/api/food_items/<category>", methods=["GET"])
def get_food_items_by_category(category):
    projection = {"_id": 1, "item_name": 1, "item_category": 1, "image_url": 1}
    documents = collection.find({"item_category": category}, projection)
    results = json_util.dumps(documents)
    return results


if __name__ == "__main__":
    app.run(debug=True)
