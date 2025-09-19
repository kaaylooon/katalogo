from flask import Blueprint, render_template
from db import *

routes = Blueprint("home", __name__)

@routes.route('/')
def home():
    businesses = mostrar_business ()
    return render_template("home.html", businesses=businesses)