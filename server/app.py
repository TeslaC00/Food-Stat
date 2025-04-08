from bson import ObjectId
from flask import Flask, flash, jsonify, redirect, request, url_for
from flask_login import LoginManager, login_user
from pymongo import ASCENDING, DESCENDING
from database import db
from ML_APIS.PredictNutritionalRating import predict_food_rating, load_model
from ML_APIS.RuleBasedRecommendation import personalize_food_recommendation
from models import User
from routes import register_routes

# Collection Database
collection = db["food_items"]
accounts_collection = db["accounts"]
users_collection = db["users"]

# Flask extension initialization
login_manager = LoginManager()
login_manager.login_view = "routes_bp.login"


@login_manager.user_loader
def load_user(user_id):
    user_doc = accounts_collection.find_one({"_id": ObjectId(user_id)})
    return User(user_doc) if user_doc else None


# Flask App Setup
app = Flask(__name__)
app.secret_key = "25_din_mai_paisa_double"  # TODO: take secret key from env

# App Logger alias
log = app.logger

# Flask extensions setup
login_manager.init_app(app)
register_routes(app)


@app.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    next_page = request.args.get("next")
    print(f"Username:{username}, password:{password}, next_page:{next_page}")
    user_doc = accounts_collection.find_one({"username": username})
    if user_doc and user_doc["password"] == password:
        print("User exists")
        login_user(User(user_doc))
        print("user logged in")
        flash(f"Logged in as {username}", "info")
        return redirect(next_page or url_for("routes_bp.profile"))
    flash("Invalid credentials", "error")
    return redirect(url_for("routes_bp.login"))


@app.post("/sign_up")
def sign_up():
    form = request.form.to_dict()
    log.info(form)

    username = form.get("username")
    password = form.get("password")

    # Check if user exists
    if accounts_collection.find_one({"username": username}):
        flash(f"{username} already exits", "info")
        return redirect(url_for("routes_bp.login"))

    # Create account without any profile
    account = {
        "username": username,
        "password": password,
        "default_profile_id": None,
        "profiles": [],
    }
    account_result = accounts_collection.insert_one(account)
    account_id = account_result.inserted_id

    # Create user profile
    profile = {
        "account_id": account_id,
        "profile_name": form.get("profile_name") or form.get("username"),
        "first_name": form.get("first_name"),
        "last_name": form.get("last_name"),
        "gender": form.get("gender"),
        "user_type": form.get("user_type"),
        "weight": float(form.get("weight", 0)),
        "height": float(form.get("height", 0)),
        "age": int(form.get("age", 0)),
        "diet_type": form.get("diet_type"),
        "allergy_info": [
            item.strip()
            for item in form.get("allergy_info", "").split(",")
            if item.strip()
        ],  # comma seperated values
        "disease_info": [
            item.strip()
            for item in form.get("disease_info", "").split(",")
            if item.strip()
        ],  # comma seperated values
    }

    profile_result = users_collection.insert_one(profile)
    profile_id = profile_result.inserted_id

    # Update account with default_profile_id and profiles list
    accounts_collection.update_one(
        {"_id": account_id},
        {"$set": {"default_profile_id": profile_id}, "$push": {"profiles": profile_id}},
    )

    flash("Account created succesfully! Please Log in")
    return redirect(url_for("routes_bp.login"))


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


@app.route("/api/profiles/<profile_id>", methods=["GET", "PUT"])  # Add PUT method
def get_user_profile(profile_id):
    users = db["users"]
    if request.method == "GET":  # Existing GET logic
        user = users.find_one(ObjectId(profile_id))
        if not user:
            return jsonify("No User Found"), 404
        user["_id"] = str(user["_id"])
        return jsonify(user)
    elif request.method == "PUT":  # New PUT logic for updates
        data = request.json
        if not data:
            return jsonify({"message": "No data provided for update"}), 400

        updated_user_data = {
            "profile_name": data.get("profile_name"),
            "firstName": data.get("firstName"),
            "lastName": data.get("lastName"),
            "gender": data.get("gender"),
            "weight": data.get("weight"),
            "height": data.get("height"),
            "age": data.get("age"),
            "userType": data.get("userType"),
            "dietType": data.get("dietType"),
            "allergy_info": data.get("allergy_info"),
            "diseases": data.get("diseases"),
        }

        try:
            users.update_one({"_id": ObjectId(profile_id)}, {"$set": updated_user_data})
            updated_user = users.find_one(ObjectId(profile_id))  # Fetch updated user
            updated_user["_id"] = str(updated_user["_id"])  # Convert ObjectId to string
            return (
                jsonify(
                    {"message": "Profile updated successfully", "profile": updated_user}
                ),
                200,
            )
        except Exception as e:
            print(f"Error updating profile: {e}")
            return jsonify({"message": "Error updating profile"}), 500


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


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """
    Returns a list of distinct food categories from the database.
    """
    categories = collection.distinct(
        "item_category"
    )  # 'collection' is your MongoDB collection object
    return jsonify(categories)


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


@app.post("/api/message")
def add_message():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    message_collection = db["message"]
    try:
        message_collection.insert_one(
            {"name": name, "email": email, "message": message}
        )
        flash("Your Message has been sent successfully", "info")
    except:
        flash("Sorry an Error Occurred! We cannot recieve your message :(", "error")
    return redirect(url_for("routes_bp.contact"))


if __name__ == "__main__":
    app.run(debug=True)
