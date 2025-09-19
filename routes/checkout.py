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

YOUR_DOMAIN = "http://192.168.0.4:5000"

@routes.route('/business/<int:business_id>/checkout', methods=['POST'])
@author_or_admin_required(buscar_id_business, "by_user")
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
				success_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/sucesso',
				cancel_url=f'{YOUR_DOMAIN}/business/{business_id}/checkout/cancelado'
			)
			return redirect(session.url, code=303)
		except Exception as e:
			logger.warning(str(e))
			return jsonify(error=str(e)), 403
	else:
		logger.info("Usuário de ID {session['user_id']} tentou acessar o checkout de um negócio de ID inválido.")
		return redirect(request.referrer or '/')

@routes.route('/business/<int:business_id>/checkout/sucesso')
@author_or_admin_required(buscar_id_business, "by_user")
def sucesso(business_id):

	logger.warning(f'Checkout com sucesso: negócio de ID {business_id} adquiriu o plano premium.')

	return render_template('sucess.html')


@routes.route('/business/<int:business_id>/checkout/cancelado')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def cancelado(business_id):

	logger.warning(f'Checkout cancelado: negócio de ID {business_id}.')

	return render_template('cancel.html')



@routes.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Corpo inválido
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Assinatura inválida
        return jsonify(success=False), 400

    # ------------------------------
    # Tratamento dos eventos
    # ------------------------------
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # pega business_id que você passou no checkout
        business_id = session.get("success_url", "").split("/")[-2]

        logger.warning(f"Pagamento concluído para business_id={business_id}")

        # chama sua função
        add_premium(True, business_id)

    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        logger.info(f"Fatura paga: {invoice['id']}")

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        logger.warning(f"Pagamento falhou: {invoice['id']}")

    return jsonify(success=True), 200