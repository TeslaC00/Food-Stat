from bson import ObjectId
import flask
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, logout_user
from database import db


routes_bp = Blueprint("routes_bp", __name__)


@routes_bp.get("/")
def index() -> Response:
    return redirect(url_for("routes_bp.home"))


@routes_bp.get("/home")
def home() -> str:
    # TODO: add database query to get data
    categories = [
        {
            "title": "Fresh Fruits",
            "desc": "Discover vitamin-rich fruits for daily nutrition",
            "img": "freshFruits.png",
            "alt": "Fresh Fruits",
        },
        {
            "title": "Vegetables",
            "desc": "Explore fiber-packed vegetable options",
            "img": "vegetables.png",
            "alt": "Vegetables",
        },
        {
            "title": "Proteins",
            "desc": "Essential proteins for muscle health",
            "img": "proteins.png",
            "alt": "Proteins",
        },
        {
            "title": "Whole Grains",
            "desc": "Nutritious grains for sustained energy",
            "img": "wholeGrains.png",
            "alt": "Grains",
        },
    ]

    return render_template("home.jinja", categories=categories)


@routes_bp.get("/category")
def category() -> str:
    # TODO: add database query to get category data
    categories_collection = db["categories"]
    items_collection = db["food_items"]

    # All categories for sidebar
    categories = list(categories_collection.find({}).sort("_id", 1))

    # Parse filters from request
    selected_categories = request.args.getlist("categories")
    selected_types = request.args.getlist("type")
    personalized = request.args.get("personalized")
    search_query = request.args.get("search", "").strip()

    query = {}

    if search_query:
        query["item_name"] = {"$regex": search_query, "$options": "i"}

    if selected_categories:
        query["item_category"] = {"$in": selected_categories}

    if "veg" in selected_types and "nonveg" not in selected_types:
        query["veg"] = True
    elif "nonveg" in selected_types and "veg" not in selected_types:
        query["veg"] = False

    # Add personal recommendation filter
    if personalized:
        if not current_user.is_authenticated:
            flash("Log in to use personalized recommendations.", "warning")
            return redirect(url_for("routes_bp.login", next=request.full_path))

        profile_id = current_user.default_profile_id
        profile = db["users"].find_one({"_id": ObjectId(profile_id)})
        if profile:
            diet_type = profile.get("diet_type")
            allergies = profile.get("allergy_info", [])
            query["diet_type"] = diet_type
            query["ingredients"] = {"$nin": allergies}

    items = list(items_collection.find(query))

    return render_template(
        "category.jinja",
        categories=categories,
        items=items,
        selected_categories=selected_categories,
        selected_types=selected_types,
        personalized=bool(personalized),
        search_query=search_query,
    )


@routes_bp.get("/food_item/<food_item_id>")
def food_item(food_item_id: str) -> str:
    items_collection = db["food_items"]

    # Fetch item from database
    food_item = items_collection.find_one({"_id": ObjectId(food_item_id)})

    if not food_item:
        flash("Food item not found.", "danger")
        return redirect(url_for("routes_bp.category"))

    return render_template("food_item.jinja", food_item=food_item)


@routes_bp.get("/contact")
def contact() -> str:
    return render_template("contact_us.jinja")


@routes_bp.get("/signup")
def sign_up() -> str:
    return render_template("signup.jinja")


@routes_bp.get("/login")
def login() -> str:
    return render_template("login.jinja")


@routes_bp.post("/logout")
@login_required
def logout() -> str:
    logout_user()
    flash("Logged out succesfully", "success")
    return redirect(url_for("routes_bp.home"))


USER_TYPE_LABELS = {
    "weight_loss": "Weight Loss",
    "weight_gain": "Weight Gain",
    "muscle_gain": "Muscle Gain",
    "pregnant_mother": "Pregnant Mother",
    "infant": "Infant",
    "general_fitness": "General Fitness",
}


@routes_bp.get("/profile")
@login_required
def profile() -> str:
    accounts_collection = db["accounts"]
    users_collection = db["users"]

    username = current_user.username

    account = accounts_collection.find_one({"username": username})
    if not account:
        flash("Account not found.", "error")
        return redirect(url_for("routes_bp.login"))

    default_profile_id = account.get("default_profile_id")
    if not default_profile_id:
        flash("No default profile set.", "warning")
        return redirect(url_for("routes_bp.login"))

    profile = users_collection.find_one({"_id": ObjectId(default_profile_id)})
    if not profile:
        flash("Profile not found", "error")
        return redirect(url_for("routes_bp.login"))
    profile["user_type"] = USER_TYPE_LABELS.get(profile.get("user_type"), "Unkown")

    return render_template("profile.jinja", user=profile)


def register_routes(app: flask.Flask) -> None:
    app.register_blueprint(routes_bp)
