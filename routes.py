from flask import Blueprint, render_template, request, flash, redirect, session, jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename

import uuid

import stripe

import json
import os
import datetime

import logging

from apirequests import get_munipicios

from db import *

from auth import *
from apirequests import *
from db.feed import mostrar_feed

stripe.api_key = "SUA_CHAVE_SECRETA"

routes = Blueprint('routes', __name__)


#logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#config de pastas
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

carousel_folder = os.path.join(UPLOAD_FOLDER, 'carousel')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(carousel_folder, exist_ok=True)

#verificar extensão permitida para img
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#página inicial
@routes.route('/')
def home():
	return render_template("home.html")

#atividades
@routes.route('/feed', methods=['GET'])
def feed():
	feed = mostrar_feed()
	meusbusinesses = []
	if 'user_id' in session:
		meusbusinesses = mostrar_businesses_user(session['user_id'])
	return render_template("feed.html", feed=feed, meusbusinesses=meusbusinesses)


@routes.route('/feed/add', methods=['POST'])
@login_required
def add_feed_route():
	business_id = request.form.get('business_id')
	content = request.form.get('content')
	image_file = request.files.get('image')

	image_path = None
	# if image_file and image_file.filename != '':
	#     filename = secure_filename(image_file.filename)
	#     image_path = f"uploads/{filename}"
	#     image_file.save(os.path.join(app.static_folder, image_path))

	add_feed(business_id, content, session['user_id'], image_path)

	logger.info(
		f"Novo feed adicionado. ID do negócio: {business_id}; "
		f"ID do usuário: {session['user_id']}"
	)

	return redirect(url_for('routes.feed'))


#pág com a listagem dos negócios
@routes.route('/businesses')
def businesses():
	search_query = request.args.get('q', '')
	categoria = request.args.get('categoria', '')
	businesses = mostrar_business(search_query, categoria)

	return render_template("businesses.html", businesses=businesses)


@routes.route('/addbusiness', methods=['GET', 'POST'])
@login_required
def addbusiness():
	if request.method == "POST":
		by_user = session.get('user_id')

		nome = request.form.get('nome')
		nome = nome.capitalize()
		descricao = request.form.get('descricao', 'Sem descrição.')
		descricao = descricao.capitalize()
		categoria = request.form.get('categoria')

		file = request.files['logo']

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_path)
		else:
			filename = None

		evento = request.form.get('evento') or None

		business_id = adicionar_business(nome, descricao, categoria, filename, by_user, evento)

		if business_id:
			logger.info(f'Novo negócio: {nome}, criado por {by_user}')
		else:
			logger.error(f"Erro na criação do negócio {nome}, tentativa por {by_user}")

		return redirect(f"/business/{business_id}")

	return render_template("addbusiness.html")


@routes.route("/get_municipios/<uf>")
def get_munipicios_route(uf):
	municipios = get_munipicios(uf)

	municipios_list = [{"nome": m["nome"]} for m in municipios]
	return jsonify(municipios_list)


@routes.route('/business/<int:business_id>')
def business(business_id):
	business = buscar_id_business(business_id)
	session_id = session.get('user_id') 

	horario = mostrar_disponivel(business_id)
	aberto = False

	now_str = datetime.datetime.now().strftime("%H:%M")

	if horario:
		abre = horario[0][3]
		fecha = horario[0][4]
		if abre <= now_str <= fecha:
			aberto = True

	comentarios = mostrar_comentarios(business_id)
	feeds = mostrar_feed_business(business_id)
	images_urls = mostrar_business_images_urls(business_id)

	if not business:
		flash('Negócio não encontrado.', 'danger')
		return redirect(url_for('routes.businesses'))

	return render_template("business.html", business=business, comentarios=comentarios, aberto=aberto, horario=horario, feeds=feeds, session_id=session_id, images_urls=images_urls)


@routes.route('/business/<int:business_id>/comentar', methods=['GET', 'POST'])
@login_required
def comentar(business_id):
	business = buscar_id_business(business_id)
	if request.method == "POST":
		content = request.form.get('content')
		add_comentario(session['user_id'],
		content, business_id)

		logger.info(f"Novo comentário no negócio de ID {business_id}, pelo usuário de ID {session['user_id']}")
		return redirect(url_for('routes.business', business_id=business_id))


@routes.route('/business/<int:business_id>/edit', methods=['GET', 'POST'])
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def edit(business_id):
	dias = [
		("dom", "Domingo"),
		("seg", "Segunda-feira"),
		("ter", "Terça-feira"),
		("qua", "Quarta-feira"),
		("qui", "Quinta-feira"),
		("sex", "Sexta-feira"),
		("sab", "Sábado")
	]
	horarios = {}
	images_urls = mostrar_business_images_urls(business_id)
	business = buscar_id_business(business_id)

	if request.method == "POST":
		#GET FORM DATA
		nome = request.form.get('nome').capitalize()
		categoria = request.form.get('categoria')
		descricao = request.form.get('descricao', 'Sem descrição.').capitalize()

		#CONTATO

		instagram = request.form.get('insta')
		if instagram and '@' not in instagram:
			instagram = f'@{instagram}'
			
		numero = request.form.get('number')
		email = request.form.get('email')

		#LOCALIZAÇÃO

		cep = request.form.get('cep')
		ruaAvenida = request.form.get('ruaAvenida')
		numeroCasa = request.form.get('numeroCasa')
		bairro = request.form.get('bairro')
		cidadeMunicipio = request.form.get('municipio')
		estado = request.form.get('estado')

		address = f'{ruaAvenida}, {numeroCasa}, {bairro}, {cidadeMunicipio}, {estado}'

		lat = None
		lon = None
		
		if address and address != 'Não informado':
			lat, lon = get_coordenadas(address)

		#LOGO

		logo_file = request.files.get('logo')

		#logo anterior
		logo_filename = business['logo_path']


		if logo_file:
			logger.info(f"Arquivo enviado: {logo_file}")
			if allowed_file(logo_file.filename):
				logger.info("Extensão permitida")

				ext = logo_file.filename.rsplit('.', 1)[1].lower()
				logo_filename = f"{uuid.uuid4().hex}.{ext}"
				logo_file.save(os.path.join(UPLOAD_FOLDER, logo_filename))
			else:
				logger.warning("Extensão não permitida")
		else:
			logger.warning("Nenhum arquivo de logo enviado")
			logo_filename = business['logo_path'] if 'logo_path' in business.keys() else None

		edit_business(business_id, nome=nome, descricao=descricao, instagram=instagram, numero=numero, email=email, logo_path=logo_filename, lat=lat, lon=lon)

		images = request.files.getlist('images[]')
		if images:
			for image in images:
				logger.info(f"Arquivo enviado: {image}")
				if allowed_file(image.filename):
					logger.info("Extensão permitida")

					ext = image.filename.rsplit('.', 1)[1].lower()
					image_filename = f"{uuid.uuid4().hex}.{ext}"
					image.save(os.path.join(UPLOAD_FOLDER, image_filename))

					add_business_images(business_id, image_filename)
					logger.info("Arquivo adicionado: {image_filename}")
				else:
					logger.warning("Extensão não permitida")
		else:
			logger.warning("Nenhum arquivo de logo enviado")

		dias_map = {"dom":0, "seg":1, "ter":2, "qua":3, "qui":4, "sex":5, "sab":6}

		for d, _ in dias:
			abre = request.form.get(f'{d}_abre')
			fecha = request.form.get(f'{d}_fecha')
			horarios[d] = (abre, fecha)
			if abre and fecha:
				for d, (abre, fecha) in horarios.items():
					dias_num = dias_map[d]
					update = update_horario(business_id, dias_num, abre, fecha)

					if not update:
						add_horario(business_id, dias_num, abre, fecha)
						logger.info(f"Horário modificado no negócio {business_id}, por {session['user_id']}")

		removed_images = request.form.get('removed_images')
		
		if removed_images:
			filenames = removed_images.split(",")
			for filename in filenames:
				# Remove do DB
				delete_business_image(business_id, image_filename=filename)
				
				# Remove do filesystem
				filepath = os.path.join(UPLOAD_FOLDER, filename)
				if os.path.exists(filepath):
					os.remove(filepath)


		logger.info(f"Negócio editado: {nome} (ID: {business_id}), pelo usuário de ID {session['user_id']}")

		return redirect(url_for('routes.business', business_id=business_id))
	return render_template('editbusiness.html', business_id=business_id, business=business, images_urls=images_urls, dias=dias)	


@routes.route('/business/<int:business_id>/del')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def delbusiness(business_id):
	business = mostrar_business_by_id(business_id)
	user_id = session.get('user_id')
	next_url = request.args.get('next') or url_for('default_page')

	if user_id == business[9]:
		del_business(business_id)
		flash('Négócio excluído com sucesso', 'sucess')
		logger.info(f"Negócio excluído: {business_id}, por {user_id}")
		return redirect(next_url)
	else:
		flash('Não foi possível excluir o negócio', 'danger')
		logger.warning(f"Erro ao tentar excluir negócio: {business_id}, por {user_id}")
		return redirect(request.referrer)


@routes.route('/business/<int:business_id>/upgrade')
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def upgrade(business_id):
	business = mostrar_business_by_id(business_id)
	return render_template('upgrade.html', business=business)


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


@routes.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
	users = mostrar_users()

	feed = mostrar_feed()

	businesses = []

	for user in users:
		user_id = user[0]
		bus_list = mostrar_businesses_user(user_id)
		if bus_list:
			businesses.extend(bus_list)
			for b in bus_list:
				comentarios = mostrar_comentarios(b[0])

	return render_template('dashboard.html', users=users, businesses=businesses, comentarios=comentarios)


@routes.route('/dashboard/business/<int:business_id>/premium', methods=['POST'])
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
@role_required('admin')
def toggle_premium(business_id):
	business = mostrar_business_by_id(business_id)
	if not business:
		flash("Negócio não encontrado.", "danger")
		return redirect(url_for('routes.dashboard'))

	novo_status = not business[13]

	add_premium(novo_status, business_id)
	action = "ativado" if novo_status else "removido"

	flash(f"Premium {action} para {business[1]}", "success")

	return redirect(url_for('routes.dashboard'))


@routes.route("/perfil/<int:user_id>")
def perfil(user_id):
	user = mostrar_user(user_id)
	business = mostrar_businesses_user(user_id)
	comentarios = mostrar_comentarios_user(user_id)

	session_id = None
	if 'user_id' in session:
		session_id = session['user_id']

	if not user:
		return "Usuário não encontrado", 404
	return render_template("perfil.html", user=user, business=business, comentarios=comentarios, session_id=session_id)


@routes.route("/perfil/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def perfiledit(user_id):
	user = mostrar_user(user_id)
	if not user:
		flash('Usuário não encontrado.', 'warning')
		return redirect('/')
	if session['user_id'] != user[0]:
		return redirect('/perfil/<int:user_id>')
	if request.method == "POST":
		username = request.form.get("username")
		descricao = request.form.get("descricao", "Sem descrição")

		edit_user(username, descricao, user_id)
		
		logger.info(f"Usuário editado: {username} (ID: {user_id}), pelo usuário de ID {session['user_id']}")
		return redirect(url_for('routes.perfil', user_id=user_id))

	return render_template("editperfil.html", user=user)