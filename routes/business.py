from flask import Blueprint, flash, render_template, request, redirect, session, url_for

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

	return render_template("businesses.html", businesses=businesses)

#adicionar business
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
		evento = request.form.get('evento') or None


		logo = request.files['logo']
		if logo and allowed_file(logo.filename):
			logo_filename = save_image(logo)
			return image_filename
		else:
			image_filename = None


		business_id = adicionar_business(nome, descricao, categoria, image_filename, by_user, evento)

		if business_id:
			logger.info(f'Novo negócio: {nome}, criado por {by_user}')
		else:
			logger.error(f"Erro na criação do negócio {nome}, tentativa por {by_user}")

		return redirect(f"/business/{business_id}")

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
	dias_map = {"dom":0, "seg":1, "ter":2, "qua":3, "qui":4, "sex":5, "sab":6}
	horarios = {}

	images_urls = mostrar_business_images_urls(business_id)
	business = buscar_id_business(business_id)

	if request.method == "POST":
		nome = request.form.get('nome').capitalize()
		categoria = request.form.get('categoria')
		descricao = request.form.get('descricao', 'Sem descrição.').capitalize()

		instagram = request.form.get('insta')
		if instagram and '@' not in instagram:
			instagram = f'@{instagram}'
			
		numero = request.form.get('number')
		email = request.form.get('email')

		cep = request.form.get('cep')
		ruaAvenida = request.form.get('ruaAvenida')
		numeroCasa = request.form.get('numeroCasa')
		bairro = request.form.get('bairro')
		cidadeMunicipio = request.form.get('municipio')
		estado = request.form.get('estado')

		address = f'{ruaAvenida}, {numeroCasa}, {bairro}, {cidadeMunicipio}, {estado}'
		
		if address and address != 'Não informado':
			lat, lon = get_coordenadas(address)

		logo = request.files.get('logo')
		logo_filename = business['logo_path']

		if logo:
			if allowed_file(logo.filename):
				logo_filename  = save_image(logo)
				return logo_filename
			else:
				logo_filename = business['logo_path'] if 'logo_path' in business.keys() else None


		edit_business(business_id, nome=nome, categoria=categoria, descricao=descricao, instagram=instagram, numero=numero, email=email, logo_path=logo_filename, lat=lat, lon=lon)

		images = request.files.getlist('images[]') or None

		if images:
			for image in images:
				if allowed_file(image.filename):
					image_filename = save_image(image)
					add_business_images(business_id, image_filename)
					logger.info("Arquivo adicionado: {image_filename}")
				else:
					logger.warning("Extensão não permitida")

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

		return redirect(url_for('business.business', business_id=business_id))
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
		return redirect(request.referrer or '/')
	else:
		flash('Não foi possível excluir o negócio', 'danger')
		logger.warning(f"Erro ao tentar excluir negócio: {business_id}, por {user_id}")
		return redirect(request.referrer or '/')


@routes.route('/business/<int:business_id>/upgrade', methods=['GET'])
@login_required
@author_or_admin_required(buscar_id_business, "by_user")
def upgrade(business_id):
	business = mostrar_business_by_id(business_id)
	return render_template('upgrade.html', business=business)
