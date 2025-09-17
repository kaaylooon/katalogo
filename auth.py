from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from db import *

auth = Blueprint('auth', __name__)


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#SIGIN, SIGNUP, LOGOUT

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		username = request.form.get('username')
		session['user'] = username

		password = request.form.get('password')

		user = verificar_user(username)	

		if user and check_password_hash(user[1], password):
			session["user_id"] = user[0]
			session["role"] = user[2]
			flash('Login feito.', 'success')
			return redirect("/")
		else:
			flash('Usuário ou senha incorretos.', "danger")
	return render_template("login.html")

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		hashed = generate_password_hash(password)

		telephone = request.form.get('number')

		#file = request.files['pfp']
		#if file and allowed_file(file.filename):
		#	filename = secure_filename(file.filename)
		#	file.save(os.path.join(UPLOAD_FOLDER, filename))

		try:
			registrar_user(username, email, hashed, telephone)
			flash('Conta criada com sucesso')
			return redirect('/login')
		except:
			flash('Usuário ou e-mail já existe.', 'danger')
	return render_template('signup.html')

@auth.route("/logout")
def logout():
	session.clear()
	flash("Deslogado com sucesso", "success")
	return redirect("/login")

#PERMISSÕES

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if "user_id" not in session:
			#flash("Você precisa logar.", "warning")
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated

def role_required(role):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			if "role" not in session or session["role"] != role:
				flash("Permissão negada.", "danger")
				return redirect("/")
			return f(*args, **kwargs)
		return decorated
	return decorator

def author_or_admin_required(model_getter, author_field="by_user"):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			obj_id = kwargs.get("business_id")
			obj = model_getter(obj_id)
			if not obj:
				return redirect('/')
			if obj[author_field] != session.get("user_id") and session.get("role") != "admin":
				flash("Sem permissão.", "danger")
				return redirect('/')
			return f(*args, **kwargs)
		return decorated
	return decorator

