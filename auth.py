from flask import Blueprint, render_template, request, redirect, url_for, flash

from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

#SIGIN, SIGNUP, LOGOUT

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		username = request.form.get('username')
		password = request.form.get('password')
		flash(f'Bem-vindo(a), {username}', 'success')
		return redirect("/")
	else:
		flash('Usuário ou senha incorretos.', "danger")
	return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		hashed = generate_password_hash(password)
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
			flash("Você precisa logar para acessar.", "warning")
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