from flask import Blueprint, render_template, request, flash, redirect, session, jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename
import os
import datetime
import logging

from apirequests import get_munipicios
from db import *
from auth import *
from apirequests import *

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
def home():
	return render_template("home.html")

@routes.route('/feed', methods=['GET', 'POST'])
def feed():
	feed = mostrar_feed()
	business = None
	
	meusbusinesses = []

	if 'user_id' in session:
		meusbusinesses = mostrar_businesses_user(session['user_id'])

	if request.method == "POST":
		if 'user_id' not in session:
			flash("Você precisa estar logado para usar esta função.", "danger")
			return redirect(url_for('auth.login'))

		business_id = request.form.get('business_id')
		content = request.form.get('content')
		image_file = request.files.get('image')

		image_path = None
		# if image_file and image_file.filename != '':
		#     filename = secure_filename(image_file.filename)
		#     image_path = f"uploads/{filename}"
		#     image_file.save(os.path.join(app.static_folder, image_path))

		add_feed(business_id, content, session['user_id'], image_path)
		business = buscar_id_business(business_id)

		logger.info(f"Novo feed por {business[1]}. ID do negócio: {business_id}; ID do usuário: {session['user_id']})")
		return redirect(url_for('routes.feed'))

	return render_template("feed.html", feed=feed, meusbusinesses=meusbusinesses, business=business)

@routes.route('/businesses')
def businesses():
	search_query = request.args.get('q', '')
	categoria = request.args.get('categoria', '')
	businesses = mostrar_business(search_query, categoria)

	return render_template("businesses.html", businesses=businesses)

@routes.route('/addbusiness', methods=['GET', 'POST'])
@login_required
def addbusiness():
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

	if request.method == "POST":
		by_user = session.get('user_id')

		#SOBRE

		nome = request.form.get('nome')
		nome = nome.capitalize()
		descricao = request.form.get('descricao', 'Sem descrição.')
		descricao = descricao.capitalize()
		categoria = request.form.get('categoria')
		
		#HORÁRIO

		for d in dias:
			abre = request.form.get(f'{d[0]}_abre')
			fecha = request.form.get(f'{d[0]}_fecha')
			horarios[d[0]] = (abre, fecha)

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

		file = request.files['logo']

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_path)
		else:
			filename = None

		images = request.files['images[]']

		if images and allowed_file(images.filename):
			filename = secure_filename(images.filename)
			images_path = os.path.join(UPLOAD_FOLDER, filename)
			images.save(images_path)
		else:
			filename = None

		#DB

		adicionar_business(nome, descricao, categoria, instagram, numero, email, filename, by_user, lat, lon)

		logger.info(f'Novo negócio: {nome}, criado por {by_user}')

		business_id = buscar_nome_business(nome)

		if not business_id:
			return redirect('/')

		dias_map = {"dom":0, "seg":1, "ter":2, "qua":3, "qui":4, "sex":5, "sab":6}

		for d, (abre, fecha) in horarios.items():
			add_horario(business_id, dias_map[d], abre, fecha)

		return redirect(f"/business/{business_id}")

	return render_template("addbusiness.html", dias=dias)

@routes.route("/get_municipios/<uf>")
def get_munipicios_route(uf):
	municipios = get_munipicios(uf)

	municipios_list = [{"nome": m["nome"]} for m in municipios]
	return jsonify(municipios_list)

#

@routes.route('/business/<int:business_id>')
def business(business_id):
	business = buscar_id_business(business_id)
	session_id = session.get('user_id') 

	horario = mostrar_disponivel(business_id)
	feeds = mostrar_feed_business(business_id)
	aberto = False	
	now_str = datetime.datetime.now().strftime("%H:%M")

	images_urls = mostrar_business_images_urls(business_id)

	if horario:
		abre = horario[0][3]
		fecha = horario[0][4]
		if abre <= now_str <= fecha:
			aberto = True

	comentarios = mostrar_comentarios(business_id)

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
def edit(business_id):
	images_urls = mostrar_business_images_urls(business_id)
	business = buscar_id_business(business_id)

	if request.method == "POST":
		#GET FORM DATA
		nome = request.form.get('nome').capitalize()
		categoria = request.form.get('categoria')
		descricao = request.form.get('descricao', 'Sem descrição.').capitalize()

		instagram = request.form.get('insta', 'Não informado')
		if instagram != 'Não informado' and '@' not in instagram:
			instagram = f'@{instagram}'
		numero = request.form.get('number', 'Não informado')
		email = request.form.get('email', 'Não informado')

		logo_file = request.files.get('logo')
		logo_filename = business['logo_path']

		if logo_file and allowed_file(logo_file.filename):
			logo_filename = secure_filename(logo_file.filename)
			logo_filepath = os.path.join(UPLOAD_FOLDER, logo_filename)
			logo_file.save(logo_filepath)
		else:
			logo_filename = business['logo_path'] if 'logo_path' in business.keys() else None

		#update business details
		edit_business(nome, categoria, descricao, instagram, numero, email, logo_filename, business_id)

		logger.info(f"Negócio editado: {nome} (ID: {business_id}), pelo usuário de ID {session['user_id']}")

		#handle carousel images upload
		if 'images' in request.files:
			carousel_files = request.files.getlist('images')
			for file in carousel_files:
				#not empty and allowed type
				if file.filename != '' and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					filepath = os.path.join(UPLOAD_FOLDER, filename)

					os.makedirs(UPLOAD_FOLDER, exist_ok=True)

					file.save(filepath)

					add_business_images(business_id, filename)

					logger.info(f"Imagens adicionadas ao negócio {business_id}, por {session['user_id']}")

		return redirect(url_for('routes.business', business_id=business_id))
	return render_template('editbusiness.html', business_id=business_id, business=business, images_urls=images_urls,)	

@routes.route('/business/<int:business_id>/del')
@login_required
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

@routes.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
	users = mostrar_users()
	businesses = None

	for user in users:
		user_id = user[0]
		businesses = mostrar_businesses_user(user_id)

	return render_template('dashboard.html', users=users, businesses=businesses)

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