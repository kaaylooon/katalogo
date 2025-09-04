from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

from db import *

routes = Blueprint('routes', __name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
def feed():
	feed = mostrar_feed()
	return render_template("feed.html", feed=feed)

@routes.route('/dashboard')
def dashboard():
	users = mostrar_users()
	return

@routes.route('/businesses')
def businesses():
	businesses = mostrar_business()
	return render_template("businesses.html", businesses=businesses)

@routes.route('/addbusiness', methods=['GET', 'POST'])
def addbusiness():
	if request.method == "POST":
		nome = request.form.get('nome')
		descricao = request.form.get('descricao', 'Sem descrição.')
		categoria = request.form.get('categoria', 'Sem categoria.')
		contato = request.form.get('contato', 'Nenhum contato informado.')
		
		file = request.files['logo']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))

		else:
			flash("Arquivo inválido", "danger")
			return redirect(request.url)

		adicionar_business(nome, descricao, categoria, contato, filename)

		return redirect("/businesses")

	return render_template("addbusiness.html")

@routes.route('/business/<int:business_id>')
def business(business_id):
	business = buscar_business(business_id)
	if not business:
		flash('Negócio não encontrado.', 'danger')
		return redirect(url_for('routes.all_businesses'))
	return render_template("business.html", business=business)



