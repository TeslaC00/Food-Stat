from bson import ObjectId
from flask import Flask, flash, jsonify, redirect, request, url_for
from flask_login import LoginManager, login_user
from pymongo import ASCENDING, DESCENDING
from database import db
from models import User
from routes import register_routes
from ML_APIS.personalizer import personalize_score
from ML_APIS.Gemini_API.fetch_ratings import get_structured_rating
from Barcode.barcode_utils import analyze_barcode_from_base64
# Collection Database
collection = db["food_items"]
users_collection = db["accounts"]

# Flask extension initialization
login_manager = LoginManager()
login_manager.login_view = "routes_bp.login"


@login_manager.user_loader
def load_user(user_id):
    user_doc = users_collection.find_one({"_id": ObjectId(user_id)})
    return User(user_doc) if user_doc else None


# Flask App Setup
app = Flask(__name__)
app.secret_key = "25_din_mai_paisa_double"  # TODO: take secret key from env

# Flask extensions setup
login_manager.init_app(app)
register_routes(app)


@app.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    next_page = request.args.get("next")
    user_doc = users_collection.find_one({"username": username})
    if user_doc and user_doc["password"] == password:
        login_user(User(user_doc))
        flash(f"Logged in as {username}", "info")
        return redirect(next_page or url_for("routes_bp.profile"))
    return "Invalid credentials"


@app.post("/sign_up")
def sign_up():
    username = request.form["username"]
    password = request.form["password"]
    print(f"Username:{username}, password:{password}")
    if users_collection.find_one({"username": username}):
        flash(f"{username} already exits", "info")
        return redirect(url_for("routes_bp.login"))
    users_collection.insert_one({"username": username, "password": password})
    flash("Account created succesfully! Log In")
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
    account = accounts.find_one(str(user_id), {"profiles": 1})

    if account is None:
        return jsonify("Error, Account not found"), 400

    data = request.json
    if data is None:
        return jsonify("Error, Please provide valid data in form"), 400

    userType = data.get("user_type", "General Fitness")
    profile_name = data.get("profile_name", "profile 1")
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


from flask import jsonify
from bson import ObjectId

@app.route("/api/food_items/category/<category>/filter/<profile_id>", methods=["GET"])
def get_food_items_by_profile(category, profile_id):
    projection = {
        "_id": 1,
        "item_name": 1,
        "item_category": 1,
        "image_url": 1,
        "final_rating": 1,
        "allergy_info": 1,
        "nutrition": 1,
        "veg": 1  # Needed for vegetarian check
    }

    users = db["users"]
    user = users.find_one(ObjectId(profile_id))
    if user is None:
        return jsonify({"Error": "User not found"}), 404

    food_items_cursor = collection.find({"item_category": category.upper()}, projection)

    # Ensure consistent formats
    user_type = user.get("userType", "general_fitness")
    user_dietType = user.get("dietType", "veg")
    user_allergies = user.get("allergy_info", [])
    user_diseases = user.get("diseases", [])

    results = []

    for item in food_items_cursor:
        base_score = item.get("final_rating", 1.5)
        nutrition = item.get("nutrition", {})
        vegFood = item.get("veg", True)
        item_allergies = item.get("allergy_info", [])

        food_item = {
            "nutrition": nutrition,
            "veg": vegFood,
            "allergy_info": item_allergies,
            "user_allergies": user_allergies  # Needed for allergy comparison
        }

        try:
            personalized_score = personalize_score(
                food_item=food_item,
                vegFood=vegFood,
                user_dict={
                    "user_type": user_type,
                    "user_allergies": user_allergies,
                    "user_diseases": user_diseases,
                    "user_dietType": user_dietType 
                },
                base_health_score=base_score
            )
        except Exception as e:
            print(f"Error scoring item '{item.get('item_name', '')}': {e}")
            personalized_score = base_score  # fallback score

        item["_id"] = str(item["_id"])
        item["personalised_score"] = personalized_score
        results.append(item)

    # Sort by personalised score (descending)
    results.sort(key=lambda x: x["personalised_score"], reverse=True)

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


@app.route("/api/form/rating",  methods=["POST"])
def get_food_item_rating(): ## GEMINI_CALLS
    data = request.json
    print(data)
    result = get_structured_rating(data)
    return jsonify({"Rating": result}), 200

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


@app.route('/upload-scan', methods=['POST'])
def upload_scan():
    try:
        data = request.get_json()
        image_data = data.get("image")
        if not image_data:
            return jsonify({"error": "No image data received"}), 400

        barcodes = analyze_barcode_from_base64(image_data)

        return jsonify({
            "message": "Barcode analysis complete",
            "barcodes": barcodes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

# for rule in app.url_map.iter_rules():
#     print(rule)