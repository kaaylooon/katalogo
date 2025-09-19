# third-party
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from auth import author_or_admin_required, login_required, role_required

# local
from db import *
from services import *

routes = Blueprint('user', __name__)

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
@author_or_admin_required(mostrar_user, "id")
def perfiledit(user_id):
	user = mostrar_user(user_id)
	if request.method == "POST":
		username = request.form.get("username")
		descricao = request.form.get("descricao", "Sem descrição")

		pfp = request.files.get('pfp')
		pfp_filename = None
		if pfp and allowed_file(pfp.filename):
			pfp_filename = save_image(pfp)

		# Só passa pfp se existir
		edit_user(username, descricao, pfp_filename, user_id)

		logger.info(f"Usuário editado: {username} (ID: {user_id}) pelo usuário de ID {session['user_id']}")
		return redirect(url_for('user.perfil', user_id=user_id))

	return render_template("editperfil.html", user=user)

#excluir user
@routes.route('/perfil/<int:user_id>/del', methods=['POST'])
@login_required
@role_required('admin')
def excluir(user_id):
	user = mostrar_user(user_id)
	if user:
		del_user(user_id)
		logger.warning(f"Usuário de ID {user_id} excluído.")

	return redirect(request.referrer or '/')