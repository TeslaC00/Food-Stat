from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import ASCENDING, DESCENDING
from database import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
collection = db["food_items"]


@app.route("/api/food_items/<id>", methods=["GET"])
def get_food_item_by_id(id):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
        "health_impact_rating": 1,
        "ingredient_quality_rating": 1,
        "nutritional_content_rating": 1,
        "nutrition": 1,
        "ingredients": 1,
    }
    
    document = collection.find_one(ObjectId(id), projection)

    if document is None:
        return jsonify({"Error": "Object not found"}), 404

    document["_id"] = str(document["_id"])

    return jsonify(document)


@app.route("/api/food_items/category/<category>", methods=["GET"])
def get_food_items_by_category(category):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
    }

    query: dict = {"item_category": category}

    # get filters
    sort_by: str = request.args.get("sort_by", "item_name")
    sort_order = DESCENDING if request.args.get("sort_order") == "desc" else ASCENDING

    documents = collection.find(query, projection).sort(sort_by, sort_order)

    results = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
