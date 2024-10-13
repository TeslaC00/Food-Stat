from flask import Flask, jsonify
from database import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
collection = db["food_items"]


@app.route("/api/food_items/<category>", methods=["GET"])
def get_food_items_by_category(category):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
        "health_impact_rating": 1,
        "ingredient_quality_rating": 1,
        "nutritional_content_rating": 1,
    }
    documents = collection.find({"item_category": category}, projection)

    results = []
    for doc in documents:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
