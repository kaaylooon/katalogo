from flask import Blueprint, Flask, jsonify, redirect, render_template, request
import stripe
import os

from db import *
from services import *
from auth import login_required, author_or_admin_required

from dotenv import load_dotenv
load_dotenv()

stripe_keys = {
	"STRIPE_API_KEY": os.environ.get('STRIPE_API_KEY'),
	"STRIPE_PUBLISHABLE_KEY": os.environ.get('STRIPE_PUBLISHABLE_KEY')
}

routes = Blueprint("checkout", __name__)

stripe.api_key = stripe_keys['STRIPE_API_KEY']
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

YOUR_DOMAIN = "https://katalogo.work"


# -------------------------
# Checkout com CARTÃO (recorrente)
# -------------------------
@routes.route('/business/<int:business_id>/checkout', methods=['POST'])
@author_or_admin_required(
    buscar_id_business,   
    author_field="by_user",
    arg_name="business_id"
)
def create_checkout_session(business_id):
	business = mostrar_business_by_id(business_id)
	if business:
		try:
			session = stripe.checkout.Session.create(
				line_items=[
					{
						'price_data': {
							"currency": "brl",
							"product_data": {
								"name": "PLANO PREMIUM",
							},
							"unit_amount": 1500,
							"recurring": {"interval": "month"}
						},
						'quantity': 1,
					}
				],
				mode='subscription',
				payment_method_types=["card", "boleto"],
				success_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/sucesso',
				cancel_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/cancelado',
				metadata={
					"business_id": str(business_id),
				},
				locale='pt-BR'
			)
			return redirect(session.url, code=303)
		except Exception as e:
			logger.warning(str(e))
			return jsonify(error=str(e)), 403
	else:
		logger.info("O usuário de ID {session['user_id']} tentou acessar checkout de um business inválido.")
		return redirect(request.referrer or '/')


# -------------------------
# Checkout com PIX (avulso, 30 dias)
# -------------------------
@routes.route('/business/<int:business_id>/checkout/pix', methods=['POST'])
@author_or_admin_required(
    buscar_id_business,   
    author_field="by_user",
    arg_name="business_id"
)
def create_checkout_session_pix(business_id):
	business = mostrar_business_by_id(business_id)
	if business:
		try:
			session = stripe.checkout.Session.create(
				line_items=[
					{
						'price_data': {
							"currency": "brl",
							"product_data": {
								"name": "Plano Premium",
							},
							"unit_amount": 1500,
							"recurring": {"interval": "month"}
						},
						'quantity': 1,
					}
				],
				mode='subscription',
				payment_method_types=["boleto"],
				success_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/sucesso',
				cancel_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/cancelado',
				metadata={
					"business_id": str(business_id),
					"payment_type": "boleto"
				},
				locale='pt-BR'
			)
			return redirect(session.url, code=303)
		except Exception as e:
			logger.warning(str(e))
			return jsonify(error=str(e)), 403
	else:
		logger.info("Usuário tentou acessar checkout de business inválido.")
		return redirect(request.referrer or '/')


# -------------------------
# Sucesso / Cancelado
# -------------------------
@routes.route('/business/<int:business_id>/checkout/sucesso')
@author_or_admin_required(
    buscar_id_business,   
    author_field="by_user",
    arg_name="business_id"
)
def sucesso(business_id):
	logger.warning(
		f"## Checkout com sucesso"
		f"ID do negócio: {business_id}"
		f"ID do usuário: {session['user_id']}"
	)
	return render_template('sucess.html', business_id=business_id)


@routes.route('/business/<int:business_id>/checkout/cancelado')
@login_required
@author_or_admin_required(
    buscar_id_business,   
    author_field="by_user",
    arg_name="business_id"
)
def cancelado(business_id):
	logger.warning(
		f"## Checkout cancelado" 
		f"ID do negócio: {business_id}"
		f"ID do usuário: {session['user_id']}"
	)

	return render_template('cancel.html')


# -------------------------
# Webhook
# -------------------------
@routes.route("/webhook", methods=["POST"])
def stripe_webhook():
	payload = request.data
	sig_header = request.headers.get('Stripe-Signature')

	try:
		event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
	except Exception as e:
		logger.warning(f'Stripe webhook error: {str(e)}')
		return str(e), 400

	# ------------------------
	# Cartão (subscription) - payment confirmed via invoice
	# ------------------------
	if event['type'] == 'invoice.paid':
		invoice = event['data']['object']
		business_id = invoice["metadata"]["business_id"]
		payment_type = invoice["metadata"].get("payment_type", "card")

		log_event(
			"## Subscription paga",
			level=logging.WARNING,
			tipo=payment_type,
			business_id=business_id
		)

		add_premium(True, business_id)  # cartão sempre libera

	# ------------------------
	# Pagamento único (boleto)
	# ------------------------
	elif event['type'] == 'payment_intent.succeeded':
		intent = event['data']['object']
		business_id = intent["metadata"]["business_id"]
		payment_type = intent["metadata"].get("payment_type")

		log_event(
			"## Pagamento único confirmado",
			level=logging.WARNING,
			tipo=payment_type,
			business_id=business_id
		)

		if payment_type == "boleto":
			add_premium(True, business_id, dias=30)

	elif event['type'] == 'customer.subscription.created':
		intent = event['data']['object']
		business_id = intent["metadata"]["business_id"]

		logger.warning(f"O negócio de ID {business_id} passou com sucesso pelo checkout.")

		log_event(
			"## Passou com sucesso pelo checkout",
			level=logging.WARNING,
			business_id=business_id
		)

	return '', 200

