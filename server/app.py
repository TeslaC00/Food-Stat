from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import ASCENDING, DESCENDING
from database import db
from flask_cors import CORS
from ML_APIS.PredictNutritionalRating import predict_food_rating, load_model
from ML_APIS.RuleBasedRecommendation import personalize_food_recommendation

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5000"])
collection = db["food_items"]


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data is None:
        return jsonify("Error, Please provide valid data in form"), 400
    username = data.get("username")
    password = data.get("password")

    accounts = db["accounts"]

    try:
        if not username or not password:
            raise ValueError

        account = accounts.find_one({"username": username}, {"password": 1, "_id": 1})
        if account is None:
            raise ValueError

        if account["password"] != password:
            raise ValueError

    except ValueError:
        return jsonify("Error, Invalid credentials"), 400

    return jsonify({"id": str(account["_id"])}), 200


@app.route("/sign_up", methods=["POST"])
def sign_up():
    data = request.json
    if data is None:
        return jsonify("Error, Please provide valid data in form"), 400
    username = data.get("username")
    password = data.get("password")
    try:
        if not username or not password:
            raise ValueError
        account = {"username": username, "password": password}
        accounts = db["accounts"]
        accounts.insert_one(account)
    except ValueError:
        return jsonify("Error, Invalid credentials"), 400

    return jsonify({"id": str(account["_id"])}), 200


@app.route("/api/user/<user_id>/profiles", methods=["GET"])
def get_user_profiles(user_id):
    accounts = db["accounts"]
    users = db["users"]
    account = accounts.find_one(ObjectId(user_id), {"profiles": 1})
    if account is None:
        return jsonify("No User Found"), 404

    profile_ids = account["profiles"]
    profiles = []
    for profile_id in profile_ids:
        user = users.find_one(ObjectId(profile_id))
        if user:
            user["_id"] = str(user["_id"])
            profiles.append(user)

    return jsonify({"profiles": profiles}), 200


@app.route("/api/user/<user_id>/profiles", methods=["POST"])
def post_user_profiles(user_id):
    accounts = db["accounts"]
    users = db["users"]
    account = accounts.find_one(ObjectId(user_id), {"profiles": 1})

    if account is None:
        return jsonify("Error, Account not found"), 400

    data = request.json
    if data is None:
        return jsonify("Error, Please provide valid data in form"), 400

    userType = data.get("user_type", "General Fitness")
    profile_name = data("profile_name", "profile 1")
    firstName = data.get("firstName", "")
    lastName = data.get("lastName", "")
    gender = data.get("gender", "Male")
    weight = data.get("weight")
    height = data.get("height")
    age = data.get("age")
    dietType = data.get("dietType")
    allergy_info = data.get("allergy_info")
    diseases = data.get("diseases")

    user = {
        "account_id": user_id,
        "userType": userType,
        "profile_name": profile_name,
        "firstName": firstName,
        "lastName": lastName,
        "gender": gender,
        "weight": weight,
        "height": height,
        "age": age,
        "dietType": dietType,
        "allergy_info": allergy_info,
        "diseases": diseases,
    }

    result = users.insert_one(user)
    accounts.update_one(
        {"_id": ObjectId(user_id)}, {"$push": {"profiles": result.inserted_id}}
    )

    return jsonify(
        {"message": "User Profile Created", "profile_id": str(result.inserted_id)}, 201
    )


@app.route("/api/profiles/<profile_id>", methods=["GET"])
def get_user_profile(profile_id):
    users = db["users"]
    user = users.find_one(ObjectId(profile_id))
    if not user:
        return jsonify("No User Found"), 404
    user["_id"] = str(user["_id"])
    return jsonify(user)


@app.route("/api/food_items/<id>", methods=["GET"])
def get_food_item_by_id(id):
    projection = {
        "_id": 1,
        "item_name": 1,
        "image_url": 1,
        "final_rating": 1,
        "health_impact_rating": 1,
        "ingredient_quality_rating": 1,
        "nutritional_content_rating": 1,
        "nutrition": 1,
        "ingredients": 1,
        "allergy_info": 1,
    }

    document = collection.find_one(ObjectId(id), projection)

    if document is None:
        return jsonify({"Error": "Object not found"}), 404

    document["_id"] = str(document["_id"])

    return jsonify(document)


@app.route("/api/food_items/<category>/filter/<profile_id>", methods=["GET"])
def get_food_items_by_profile(category, profile_id):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
        "allergy_info": 1,
    }
    users = db["users"]
    user = users.find_one(ObjectId(profile_id))
    if user is None:
        return jsonify({"Error": "Object not found"}), 404

    food_items_list = personalize_food_recommendation(
        category=category,
        user_type=user["userType"],
        sex=user["gender"],
        height=user["height"],
        weight=user["weight"],
        age=user["age"],
    )

    results = []

    for food_items in food_items_list:
        name = food_items[0]
        personalised_score = food_items[1]
        document = collection.find_one({"item_name": name}, projection)
        if document is not None:
            document["_id"] = str(document["_id"])
            document["personalised_score"] = personalised_score
            results.append(document)

    results = sorted(results, key=lambda x: x["personalised_score"], reverse=True)
    return jsonify(results)


@app.route("/api/food_items/category/<category>", methods=["GET"])
def get_food_items_by_category(category):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
        "allergy_info": 1,
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


@app.route("/api/food_items/rating", methods=["POST"])
def get_food_item_rating():
    keys = [
        "NUTRITION.ENERGY",  # Example energy value
        "NUTRITION.PROTEIN",  # Example protein value
        "NUTRITION.CARBOHYDRATE",  # Example carbs value
        "NUTRITION.TOTAL_SUGARS",  # Example sugars value
        "NUTRITION.ADDED_SUGARS",  # Example added sugars value
        "NUTRITION.TOTAL_FAT",  # Example fat value
        "NUTRITION.SATURATED_FAT",  # Example saturated fat value
        "NUTRITION.FIBER",  # Example fiber value
        "NUTRITION.SODIUM",  # Example sodium value
    ]
    data = request.json
    print(data)
    if data is None:
        return jsonify("Error, Please provide valid data in form"), 400
    nutrition_info = {}
    for key in keys:
        nutrition_info[key] = int(data.get(key, 0))

    nutrition_model = load_model("ML_APIS/pipeline.joblib")
    rating = predict_food_rating(input_data=nutrition_info, model=nutrition_model)
    print("Type of rating:", type(rating))
    return jsonify({"Rating": rating}), 200


if __name__ == "__main__":
    app.run(debug=True)
