from flask import Blueprint, redirect, render_template, url_for
import stripe
from auth import author_or_admin_required, login_required
from db import *
from services import *

routes = Blueprint('checkout', __name__)


stripe.api_key = "SUA_CHAVE_SECRETA"


@routes.route('/checkout/<int:business_id>')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def checkout(business_id):
	business = mostrar_business_by_id(business_id)
	return 'hello'


@routes.route('/checkout/<int:business_id>/card')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def checkout_card(business_id):
	business = mostrar_business_by_id(business_id)
	session = stripe.checkout.Session.create(
			payment_method_types=['card'],
			line_items=[{
				'price_data': {
				'currency': 'brl',
				'product_data': {'name': f'Plano Premium - Business {business_id}'},
				'unit_amount': 1500,  # R$15,00 em centavos
				'recurring': {'interval': 'month'}
			},
			'quantity': 1,
		}],
		mode='subscription',
		success_url=url_for('routes.checkout_success', business_id=business_id, _external=True),
		cancel_url=url_for('routes.checkout_cancel', business_id=business_id, _external=True),
		client_reference_id=str(business_id)
	)
	return redirect(session.url)


@routes.route('/checkout/<int:business_id>/success')
@author_or_admin_required(buscar_id_business, "by_user")
@login_required
def checkout_success(business_id):
	business = mostrar_business_by_id(business_id)
	premium = True
	add_premium(premium, business_id)
	return render_template('checkout_success.html', business=business)


@routes.route('/checkout/<int:business_id>/cancel')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def checkout_cancel(business_id):
	business = mostrar_business_by_id(business_id)
	return ''
