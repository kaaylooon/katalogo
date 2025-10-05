from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

from services import *
from db import *

auth = Blueprint('auth', __name__)

@auth.route("/check_username")
def check_username():
	username = request.args.get("username")
	exists = bool(verificar_user(username))
	return {"exists": exists}

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')

		user = verificar_user(username) 

		if user and check_password_hash(user['password'], password):
			session["user_id"] = user['id']
			session["role"] = user['role']
			session['username'] = username
			
			log_event(
				" Login bem-sucedido",
				level=logging.INFO,
				username=username,
				ip=request.remote_addr
				)

			return redirect('/')
		else:  
			flash('Usuário ou senha incorretos.', "danger")

			log_event(
				" Tentativa falha de login",
				level=logging.INFO,
				username=username,
				ip=request.remote_addr
				)

	return render_template("login.html")


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		hashed = generate_password_hash(password)
		telephone = request.form.get('number')

		try:
			registrar_user(username, email, hashed, telephone)

			log_event(
				" Novo usuário registrado",
				level=logging.INFO,
				username=username,
				email=email
			)

			return redirect('/login')

		except psycopg2.IntegrityError as e:
			flash('Usuário ou e-mail já existe.', 'danger')

			log_event(
				" Erro de integridade ao registrar usuário",
				level=logging.WARNING,
				username=username,
				email=email,
				motivo=f"{str(e)}"
			)

		except Exception as e:
			flash(f'Ocorreu um erro inesperado: {e}', 'danger')

			log_event(
				" Erro de integridade ao registrar usuário",
				level=logging.WARNING,
				motivo=f"{str(e)}"
			)

	return render_template('signup.html')


@auth.route("/logout")
def logout():
	session.clear()
	return redirect("/login")


# ------------------------
# DECORATORS DE PERMISSÃO
# ------------------------

def login_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if "user_id" not in session:
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated


def role_required(role):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			if "role" not in session or session["role"] != role:
				flash("Permissão negada.", "danger")

				log_event(
					" Permissão negada (tentou acessar uma área não permitida para o seu cargo)",
					level=logging.INFO,
					user_id=session.get('user_id'),
					cargo=session.get('role')
				)
				return redirect(request.referrer or '/')
			return f(*args, **kwargs)
		return decorated
	return decorator


def author_or_admin_required(model_getter, author_field="by_user", arg_name="id"):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			obj_id = kwargs.get(arg_name)
			obj = model_getter(obj_id)
			if not obj:
				return redirect('/')
			if obj[author_field] != session.get("user_id") and session.get("role") != "admin":
				flash("Permissão negada.", "danger")

				log_event(
					" Permissão negada",
					level=logging.INFO,
					user_id=session.get('user_id'),
					cargo=session.get('role')
				)
				return redirect(request.referrer or '/')
			return f(*args, **kwargs)
		return decorated
	return decorator
