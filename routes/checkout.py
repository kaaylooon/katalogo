from flask import Blueprint, Flask, jsonify, redirect, request
import stripe


import os
from dotenv import load_dotenv
load_dotenv()
stripe_keys = {
	"STRIPE_API_KEY": os.environ.get('STRIPE_API_KEY'),
	"STRIPE_PUBLISHABLE_KEY": os.environ.get('STRIPE_PUBLISHABLE_KEY')
}

routes = Blueprint("checkout", __name__)

stripe.api_key = stripe_keys['STRIPE_API_KEY']

YOUR_DOMAIN = "http://127.0.0.1:5000"

@routes.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
	try:
		session = stripe.checkout.Session.create(
			line_items=[
				{
					'price_data': {
						"currency": "brl",
						"product_data": {
							"name": "Katálogo: PLANO PREMIUM",
						},
						"unit_amount": 1500,
						"recurring": {'interval':
							'month'}
					},
					'quantity': 1,
				}
			],
			mode='subscription',
			success_url=YOUR_DOMAIN,
			cancel_url=YOUR_DOMAIN,
		)
		return redirect(session.url, code=303)
	except Exception as e:
		return jsonify(error=str(e)), 403