from flask import Blueprint, render_template, request, flash, redirect, session
from werkzeug.utils import secure_filename
import os

from db import *
from auth import *

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
def home():
	return render_template("home.html")

@routes.route('/feed')
def feed():
	feed = mostrar_feed()
	return render_template("feed.html", feed=feed)

@routes.route('/addfeed', methods=['GET', 'POST'])
@login_required
def addfeed():

	return redirect(url_for('routes.feed'))
	return render_template("addfeed.html")

@routes.route('/businesses')
def businesses():
	search_query = request.args.get('q', '')
	businesses = mostrar_business(search_query)
	return render_template("businesses.html", businesses=businesses)

@routes.route('/addbusiness', methods=['GET', 'POST'])
@login_required
def addbusiness():
	if request.method == "POST":
		nome = request.form.get('nome')
		descricao = request.form.get('descricao', 'Sem descrição.')

		categoria = request.form.get('categoria', 'Sem categoria.')

		contato = request.form.getlist('contato[]')
		contato = ','.join(contato)

		if not contato:
			contato = "Nenhum contato informado."
		
		file = request.files['logo']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))

		else:
			flash("Arquivo inválido", "danger")
			return redirect(request.url)

		by_user = session.get('user_id')

		adicionar_business(nome, descricao, categoria, contato, filename, by_user)

		business_id = buscar_nome_business(nome)
		if not business_id:
			return redirect('/')

		return redirect(f"/business/{business_id}")

	return render_template("addbusiness.html")

@routes.route('/business/<int:business_id>')
def business(business_id):
	business = buscar_id_business(business_id)
	if not business:
		flash('Negócio não encontrado.', 'danger')
		return redirect(url_for('routes.businesses'))
	return render_template("business.html", business=business)

@routes.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
	users = mostrar_users()
	return render_template('dashboard.html', users=users)

@routes.route("/perfil/<int:user_id>")
@login_required
def perfil(user_id):
	print(user_id)
	print(session["user_id"])
	user = mostrar_user(user_id)
	business = mostrar_businesses_user(user_id)
	if not user:
		return "Usuário não encontrado", 404
	return render_template("perfil.html", user=user, business=business)
