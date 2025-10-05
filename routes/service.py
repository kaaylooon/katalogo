from flask import Blueprint, render_template, request
from db import *
from services import *

routes = Blueprint('service', __name__)

@routes.route('/services')
def services():
	search_query = request.args.get('q', '')
	categoria = request.args.get('categoria', '')
	businesses = mostrar_business(search_query, categoria)

	return render_template("services.html", businesses=businesses, mode="servicos")
