from flask import Blueprint, render_template

routes = Blueprint("home", __name__)

@routes.route('/')
def home():
    return render_template("home.html")