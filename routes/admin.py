from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request, session
from auth import login_required, role_required
from db import *
from services import *
from datetime import datetime, timedelta
import uuid 

routes = Blueprint('admin', __name__)


usuarios_ativos = {}

@routes.before_request
def registrar_sessao():
	# Cria um session_id único se ainda não existir
	if 'session_id' not in session:
		session['session_id'] = str(uuid.uuid4())

	session_id = session['session_id']
	usuarios_ativos[session_id] = datetime.now()

@routes.route("/online")
def online():
	agora = datetime.now()
	# filtra só quem acessou nos últimos 5 minutos
	ativos = {sid: t for sid, t in usuarios_ativos.items() if agora - t < timedelta(minutes=5)}

	# limpa o dicionário dos inativos
	usuarios_ativos.clear()
	usuarios_ativos.update(ativos)

	usuarios_online = len(ativos)

	return f"Usuários online: {usuarios_online}"


@routes.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
	users = mostrar_users()
	feed = mostrar_feed()
	comentarios = mostrar_comentarios()

	total_businesses = len(mostrar_business())
	total_comentarios = len(mostrar_comentarios())
	total_feeds = len(mostrar_feed())
	total_users = len(mostrar_users())

	premium_count = sum(1 for b in mostrar_business() if b['premium'])

	businesses = []
	for user in users:
		user_id = user['id']
		bus_list = mostrar_businesses_user(user_id)
		if bus_list:
			businesses.extend(bus_list)

	agora = datetime.now()
	ativos = {sid: t for sid, t in usuarios_ativos.items() if agora - t < timedelta(minutes=5)}
	usuarios_ativos.clear()
	usuarios_ativos.update(ativos)
	usuarios_online = len(ativos)

	return render_template(
		'dashboard.html',
		users=users,
		feed=feed,
		businesses=businesses,
		comentarios=comentarios,
		total_businesses=total_businesses,
		total_comentarios=total_comentarios,
		total_feeds=total_feeds,
		total_users=total_users,
		premium_count=premium_count,
		usuarios_ativos=usuarios_ativos
	)

@routes.route("/api/businesses")
def api_businesses():
	businesses = [serialize_business(b) for b in mostrar_business()]
	return jsonify({"data": businesses})

@routes.route("/api/users")
def api_users():
	users = [serialize_user(u) for u in mostrar_users()]
	return jsonify({"data": users})

@routes.route("/api/comments")
def api_comments():
	comments = [serialize_comment(c) for c in mostrar_comentarios()]
	return jsonify({"data": comments})

@routes.route("/api/feeds")
def api_feeds():
	feeds = [serialize_feed(f) for f in mostrar_feed()]
	return jsonify({"data": feeds})

@routes.route('/dashboard/business/<int:business_id>/premium', methods=['POST'])
@login_required
@role_required('admin')
def toggle_premium(business_id):
	business = mostrar_business_by_id(business_id)
	if not business:
		flash("Negócio não encontrado.", "danger")
		return redirect(request.referrer or '/')
	novo_status = not bool(business['premium'])
	add_premium(novo_status, business_id)
	action = "ativado" if novo_status else "removido"
	flash(f"Premium {action} para {business['nome']}", "success")
	return redirect(request.referrer or url_for('admin.dashboard'))