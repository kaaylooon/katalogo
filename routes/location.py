from flask import Blueprint, jsonify

from services.location_service import get_municipios

routes = Blueprint("location", __name__)

@routes.route("/get_municipios/<uf>")
def get_municipios_route(uf: str):
	return jsonify(get_municipios(uf))
