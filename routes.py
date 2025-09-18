
# built-ins
import uuid
import json
import os
import datetime
import logging

# third-party
import stripe
from flask import Blueprint, render_template, request, flash, redirect, session, jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename

# local

from db import *
from db.feed import mostrar_feed
from auth import *
from apirequests import *
from services import *

routes = Blueprint('routes', __name__)


@routes.route("/get_municipios/<uf>")
def get_munipicios_route(uf):
	municipios = get_munipicios(uf)

	municipios_list = [{"nome": m["nome"]} for m in municipios]
	return jsonify(municipios_list)


@routes.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
	payload = request.data
	sig_header = request.headers.get('Stripe-Signature')
	endpoint_secret = "SUA_CHAVE_ENDPOINT_WEBHOOK"

	try:
		event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
	except Exception as e:
		return str(e), 400

	# Assinatura criada / paga
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		business_id = int(session['client_reference_id'])
		business = mostrar_business_by_id(business_id)
		premium = True
		add_premium(premium, business_id)

	return '', 200
