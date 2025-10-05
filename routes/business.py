from flask import Blueprint, flash, render_template, request, redirect, session, url_for
from flask_limiter import RateLimitExceeded

from apirequests import get_coordenadas
from auth import author_or_admin_required, login_required
from db import *
from services import *

routes = Blueprint('business', __name__)

@routes.route('/businesses')
def businesses():
	search_query = request.args.get('q', '')
	categoria = request.args.get('categoria', '')
	businesses = mostrar_business(search_query, categoria)

	return render_template("businesses.html", businesses=businesses, mode="negocios")

#adicionar business
@routes.route('/addbusiness', methods=['GET', 'POST'])
@login_required
@limiter.limit("3 per hour", methods=["POST"])
def addbusiness():
	try:
		if request.method == "POST":
			by_user = session.get('user_id')
			nome = request.form.get('nome', 'Anônimo')
			nome = nome[0].upper() + nome[1:]

			descricao = request.form.get('descricao', 'Sem descrição.')
			descricao = descricao[0].upper() + descricao[1:]
			
			categoria = request.form.get('categoria')
			
			instagram = request.form.get('insta', None)
			if instagram:
				if '@' not in instagram:
					instagram = f"@{instagram}"
			numero = request.form.get('number', None)
			evento = request.form.get('evento') or None
			integrantes = request.form.get('integrantes')


			logo = request.files['logo']
			if logo and allowed_file(logo.filename):
				logo_filename = save_image(logo)
			else:
				logo_filename = None

			business_id = adicionar_business(nome, descricao, categoria, instagram, numero, logo_filename, by_user, evento, integrantes)

			if business_id:
				logger.info(
					f" Novo negócio"
					f"Nome do negócio: {nome}"
					f"ID do usuário: {by_user}")

				add_notification(by_user, f"Negócio {nome} cadastrado com sucesso! Para editar as  informações, basta acessar a página do negócio e clicar no botão da direita inferior.")
			else:
				logger.error(
					f" Erro na criação de negócio"
					f"Nome do negócio: {nome}"
					f"ID do usuário: {by_user}"
				)
			return redirect(f"/business/{business_id}")

	except RateLimitExceeded:
		flash("Você atingiu o limite de envios. Tente novamente mais tarde.", "warning")

		negociosDoUsuario = mostrar_businesses_user(session['user_id'])
		logger.warning(
			f" Usuário atingiu o limite de criação de negócios por hora"
			f"ID do usuário: {session['user_id']}"
			f"Negócios cadastrados pelo usuário: {negociosDoUsuario}"
		)
		return redirect(url_for("business.businesses"))

	return render_template("addbusiness.html")


@routes.route('/business/<int:business_id>')
def business(business_id):
	business = buscar_id_business(business_id)
	session_id = session.get('user_id') 
	horario_de_funcionamento = mostrar_disponivel(business_id)

	aberto = None
	if horario_de_funcionamento:
		aberto = verificar_disponibilidade(horario_de_funcionamento) #boolean

	comentarios = mostrar_comentarios_business(business_id)
	
	feeds = mostrar_feed_business(business_id)
	images_urls = mostrar_business_images_urls(business_id)

	if not business:
		flash('Negócio não encontrado.', 'danger')
		return redirect(request.referrer or '/')

	return render_template("business.html", business=business, comentarios=comentarios, aberto=aberto, horario=horario_de_funcionamento, feeds=feeds, session_id=session_id, images_urls=images_urls)


@routes.route('/business/<int:business_id>/edit', methods=['GET', 'POST'])
@login_required
@author_or_admin_required(
	buscar_id_business,   
	author_field="by_user",
	arg_name="business_id"
)
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
	dias_map = {"dom":0, "seg":1, "ter":2, "qua":3, "qui":4, "sex":5, "sab":6}
	horarios = {}
	fechado_status = {}

	images_urls = mostrar_business_images_urls(business_id)
	business = buscar_id_business(business_id)

	if request.method == "POST":
		nome = request.form.get('nome')
		nome = nome[0].upper() + nome[1:]

		categoria = request.form.get('categoria')
		descricao = request.form.get('descricao', 'Sem descrição.')
		descricao = descricao[0].upper() + descricao[1:]

		instagram = request.form.get('insta')
		if instagram and '@' not in instagram:
			instagram = f'@{instagram}'
			
		numero = request.form.get('number')
		email = request.form.get('email')

		cep = request.form.get('cep')
		ruaAvenida = request.form.get('ruaAvenida')
		numeroCasa = request.form.get('numeroCasa')
		bairro = request.form.get('bairro')
		municipio = request.form.get('municipio')
		estado = request.form.get('estado')
		
		lat, lon = None, None
		address = f'{ruaAvenida}, {numeroCasa}, {municipio} - {estado}, Brasil'
			
		if all([ruaAvenida, numeroCasa, municipio, estado]):
			lat, lon = get_coordenadas(address)
			if lat is not None:
				lat, lon = float(lat), float(lon)

		if not lat or not lon:
			if cep:
				localization_data = get_cep(cep)
				if isinstance(localization_data, dict) and 'lat' in localization_data and 'lng' in localization_data:
					lat = localization_data['lat']
					lon = localization_data['lng']

		logo = request.files.get('logo')
		logo_filename = business['logo_path']

		if logo:
			if allowed_file(logo.filename):
				logo_filename  = save_image(logo)
			else:
				logo_filename = business.get('logo_path')


		edit_business(business_id, nome=nome, categoria=categoria, descricao=descricao, instagram=instagram, numero=numero, email=email, logo_path=logo_filename, lat=lat, lon=lon, address=address)

		images = request.files.getlist('images[]') or None

		if images:
			for image in images:
				if allowed_file(image.filename):
					image_filename = save_image(image)
					add_business_images(business_id, image_filename)

					log_event(
						" Arquivo adicionado",
						level=logging.INFO,
						negocio=f"{nome} (ID: {business_id})",
						user_id=session['user_id']
						)

				else:
					flash("Extensão de arquivo não permitida", 'danger')

					log_event(
						" Extensão de arquivo não permitida",
						level=logging.WARNING,
						imagem=image.filename,
						negocio=f"{nome} (ID: {business_id})",
						user_id=session["user_id"]
					)

		for d, _ in dias:
			abre = request.form.get(f'{d}_abre')
			fecha = request.form.get(f'{d}_fecha')
			fechado = request.form.get(f'{d}_fechado')

			horarios[d] = (abre, fecha)
			fechado_status[d] = fechado is not None

		for d, (abre, fecha) in horarios.items():
			dias_num = dias_map[d]

			if fechado_status[d]:
				del_horario(business_id, dias_num)
			elif abre and fecha:
				
				update = update_horario(business_id, dias_num, abre, fecha)
				if not update:
					add_horario(business_id, dias_num, abre, fecha)

		removed_images = request.form.get('removed_images')
		
		if removed_images:
			filenames = removed_images.split(",")
			for filename in filenames:
				# Remove do DB
				delete_business_image(business_id, filename)
				
				# Remove do filesystem
				filepath = os.path.join(UPLOAD_FOLDER, filename)
				if os.path.exists(filepath):
					os.remove(filepath)

		log_event(
			" Negócio editado",
			level=logging.INFO,
			negocio=f"{nome} (ID: {business_id})",
			user_id=session['user_id']
		)

		return redirect(url_for('business.business', business_id=business_id))
	return render_template('editbusiness.html', business_id=business_id, business=business, images_urls=images_urls, dias=dias)	


@routes.route('/business/<int:business_id>/del', methods=['GET', 'POST'])
@login_required
@author_or_admin_required(
	buscar_id_business,   
	author_field="by_user",
	arg_name="business_id"
)
def delbusiness(business_id):
	del_business(business_id)
	flash('Négócio excluído com sucesso', 'sucess')

	log_event(
			" Negócio excluído",
			level=logging.INFO,
			business_id=business_id,
			user_id=session['user_id']
		)

	return redirect(request.referrer or '/')

@routes.route('/business/<int:business_id>/upgrade', methods=['GET'])
@login_required
@author_or_admin_required(
	buscar_id_business,   
	author_field="by_user",
	arg_name="business_id"
)
def upgrade(business_id):
	business = mostrar_business_by_id(business_id)
	return render_template('upgrade.html', business=business)
