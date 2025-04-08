import flask
from database import db
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required, logout_user
from bson import ObjectId


collection = db["food_items"]
users_collection = db["accounts"]

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

    food_items = [
        {
            "id": 1,
            "title": "Green Apple",
            "desc": "Crisp and sweet organic green apples.",
            "image_url": "https://media.istockphoto.com/id/629734762/photo/green-apple-with-leaf-isolated-on-white-clipping-path-included.jpg?s=1024x1024&w=is&k=20&c=QzSTeGlb1GkZWQ0O2VBlAeB8-ZYPzXFv7YSUYxE2AoI=",
            "alt": "Green Apple",
        },
        {
            "id": 2,
            "title": "Red Apple",
            "desc": "Crisp and sweet organic red apples.",
            "image_url": "https://media.istockphoto.com/id/614871876/photo/apple-isolated-on-wood-background.jpg?s=1024x1024&w=is&k=20&c=HlmdzA8HWMiVdSicwDiEa77FSxQEEvxm6nGzeSRGBZ4=",
            "alt": "Red Apple",
        },
        {
            "id": 3,
            "title": "Pasta",
            "desc": "Restaurant level delicious pasta.",
            "image_url": "https://media.istockphoto.com/id/482964545/photo/arrabiata-pasta.jpg?s=1024x1024&w=is&k=20&c=WV35LbX2fkLqb2jYSPqFQcyN0OlbF_HAJ0tWbfQ9KzA=",
            "alt": "Pasta",
        },
        {
            "id": 4,
            "title": "Noodles",
            "desc": "Long, slippery and saucy noooodles.",
            "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=1292&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "alt": "Noodles",
        },
    ]

    return render_template("category.jinja", food_items=food_items)


@routes_bp.get("/food_item/<int:food_item_id>")
def food_item(food_item_id: int) -> str:
    # TODO: add database query to get food item data

    food_items = [
        {
            "id": 1,
            "title": "Green Apple",
            "image_url": "https://media.istockphoto.com/id/629734762/photo/green-apple-with-leaf-isolated-on-white-clipping-path-included.jpg?s=1024x1024&w=is&k=20&c=QzSTeGlb1GkZWQ0O2VBlAeB8-ZYPzXFv7YSUYxE2AoI=",
            "alt": "Green Apple",
            "rating": 1,
            "energy": 1,
            "ingredients": ["Hara", "Apple"],
            "allergies": ["Hara ranga"],
        },
        {
            "id": 2,
            "title": "Red Apple",
            "image_url": "https://media.istockphoto.com/id/614871876/photo/apple-isolated-on-wood-background.jpg?s=1024x1024&w=is&k=20&c=HlmdzA8HWMiVdSicwDiEa77FSxQEEvxm6nGzeSRGBZ4=",
            "alt": "Red Apple",
            "rating": 4.0,
            "energy": 11,
            "protein": 30,
            "carbs": 50,
            "fat": 100,
            "ingredients": [],
            "allergies": [],
        },
        {
            "id": 3,
            "title": "Pasta",
            "image_url": "https://media.istockphoto.com/id/482964545/photo/arrabiata-pasta.jpg?s=1024x1024&w=is&k=20&c=WV35LbX2fkLqb2jYSPqFQcyN0OlbF_HAJ0tWbfQ9KzA=",
            "alt": "Pasta",
            "rating": 3.5,
            "energy": 100,
            "carbs": 6,
            "fat": 22,
            "ingredients": ["Sauce", "Namak", "Masala", "Atta"],
            "allergies": ["Poink", "Oink", "Khujli"],
        },
        {
            "id": 4,
            "title": "Noodles",
            "image_url": "https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=1292&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            "alt": "Noodles",
            "rating": 4.5,
            "energy": 1,
            "protein": 23,
            "carbs": 20,
            "fat": 202,
            "ingredients": ["Lamba Atta", "Chota masala", "Peela oil"],
            "allergies": ["Nuinui", "Nainai"],
        },
    ]

    food_item = food_items[food_item_id - 1]

    return render_template("food_item.jinja", food_item=food_item)


@routes_bp.get("/contact")
def contact() -> str:
    return render_template("contact_us.jinja")


@routes_bp.get("/aboutus")
def about_us() -> str:
    return render_template("about_us.jinja")


@routes_bp.get("/doc")
def doc_consultation() -> str:
    return render_template("doc_consul.jinja")


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


@routes_bp.get("/profile/<profile_id>")  # Route now takes profile_id as URL parameter
@login_required
def profile(profile_id) -> str:
    user_profile = users_collection.find_one({"_id": ObjectId(profile_id)}) # Fetch profile from DB
    if not user_profile:
        flash("Profile not found.", "error") # Handle case where profile is not found
        return redirect(url_for('routes_bp.home')) # Redirect to home or login

    user_profile["_id"] = str(user_profile["_id"]) # Convert ObjectId to string for Jinja

    return render_template("profile.jinja", user_profile=user_profile) # Pass user_profile to template

def register_routes(app: flask.Flask) -> None:
    app.register_blueprint(routes_bp)
