import flask
from flask import Blueprint, Response, redirect, render_template, url_for


routes_bp = Blueprint("routes_bp", __name__)


@routes_bp.get("/")
def index() -> Response:
    return redirect(url_for("routes_bp.home"))


@routes_bp.get("/home")
def home() -> str:
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
    # return render_template("category.html")
    # return render_template("food_item.html")
    # return render_template("contact_us.html")
    # return render_template("home.html")


def register_routes(app: flask.Flask) -> None:
    app.register_blueprint(routes_bp)
