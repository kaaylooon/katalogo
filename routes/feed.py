
# third-party
from flask import Blueprint, redirect, render_template, request, session, url_for

# local
from auth import allowed_file, author_or_admin_required, login_required
from db import *
from services import *

routes = Blueprint('feed', __name__)

#atividades
@routes.route('/feed', methods=['GET'])
def feed():
	feed = mostrar_feed()
	meusbusinesses = []
	if 'user_id' in session:
		meusbusinesses = [b for b in mostrar_businesses_user(session['user_id']) if b[5]]

	return render_template("feed.html", feed=feed, meusbusinesses=meusbusinesses)

#adicionar feed
@routes.route('/feed/add', methods=['POST'])
@login_required
def add():
	business_id = request.form.get('business_id')
	content = request.form.get('content')
	image = request.files.get('image')

	if image and allowed_file(image.filename):
		image_filename = save_image(image)
	else:
		image_filename = None

		add_feed(business_id, content, session['user_id'], image_filename)

	logger.info(
		f"Novo feed adicionado. ID do negócio: {business_id}; "
		f"ID do usuário: {session['user_id']}"
	)

	return redirect(request.referrer or '/')
	
#excluir feed
@routes.route('/feed/<int:feed_id>/del', methods=['POST'])
@login_required
@author_or_admin_required
def del_feed_route(feed_id):
	feed = mostrar_feed_by_id(feed_id)
	if feed:
		del_feed(feed_id)
		logger.warning(f"Feed do negócio de ID {feed[1]} excluído pelo usuário de ID {session['user_id']}. Conteúdo: {feed[2]}")

	return redirect(request.referrer or '/')