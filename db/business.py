import sqlite3
from .connection import get_connection

def adicionar_business(nome, descricao, categoria, filename, by_user, evento):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO business (nome, descricao, categoria, instagram, numero, email, logo_path, by_user, lat, lon, evento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, descricao, categoria, '', '', '', filename, by_user, '', '', evento))

	business_id = cur.lastrowid
	conn.commit()
	conn.close()
	return business_id

def edit_business(nome, descricao, categoria, instagram, numero, email, filename, lat, lon, business_id):
	with get_connection() as conn:
		cur = conn.cursor()
		cur.execute("""
			UPDATE business
			SET nome = ?, categoria = ?, descricao = ?, instagram = ?, numero = ?, email = ?, logo_path = ?, lat = ?, lon = ?
			WHERE id = ?
		""", (nome, categoria, descricao, instagram, numero, email, filename, lat, lon, business_id))
		conn.commit()

def del_business(business_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM business WHERE id = ?", (business_id,))
	conn.commit()
	conn.close()

def buscar_id_business(business_id):
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM business WHERE id = ?", (business_id,))
	business = cur.fetchone()
	conn.close()
	return business


def mostrar_business(search_query='', categoria=''):
	conn = get_connection()
	cur = conn.cursor()

	query = "SELECT * FROM business WHERE 1=1"
	params = []

	if search_query:
		query += " AND nome LIKE ?"
		params.append(f"%{search_query}%")

	if categoria:
		query += " AND categoria = ?"
		params.append(categoria)

	query += " ORDER BY premium DESC, added_at DESC"

	cur.execute(query, params)
	businesses = cur.fetchall()

	conn.close()
	return businesses

def buscar_nome_business(nome):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id FROM business WHERE nome = ?", (nome,))
	business = cur.fetchone()
	conn.close()
	return business[0] if business else None

def mostrar_business_by_id(business_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM business WHERE id = ?", (business_id,))
	business = cur.fetchone()
	conn.close()
	return business

def mostrar_businesses_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, nome, logo_path, added_at, by_user, premium FROM business WHERE by_user = ?", (user_id,))
	meusbusinesses = cur.fetchall()
	conn.close()
	return meusbusinesses

def add_premium(premium, business_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		UPDATE business
		SET premium = ?
		WHERE id = ?
	""", (premium, business_id))
	conn.commit()
	conn.close()
