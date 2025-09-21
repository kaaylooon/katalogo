import sqlite3
from .connection import get_connection
import datetime

def adicionar_business(nome, descricao, categoria, instagram, numero, filename, by_user, evento):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO business (nome, descricao, categoria, instagram, numero, email, logo_path, by_user, lat, lon, evento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, descricao, categoria, instagram, numero, '', filename, by_user, '', '', evento))

	business_id = cur.lastrowid
	conn.commit()
	conn.close()
	return business_id

def edit_business(business_id, **kwargs):
	allowed_fields = ['nome', 'categoria', 'descricao', 'instagram', 'numero', 'email', 'logo_path', 'lat', 'lon', 'address']
	set_clause = []
	params = []

	for field in allowed_fields:
		if field in kwargs and kwargs[field] not in [None, '']:
			set_clause.append(f"{field} = ?")
			params.append(kwargs[field])

	if not set_clause:
		return  # nada pra atualizar

	params.append(business_id)
	query = f"UPDATE business SET {', '.join(set_clause)} WHERE id = ?"

	with get_connection() as conn:
		conn.execute(query, tuple(params))
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


def desativar_premium_expirado():
	hoje = datetime.date.today()
	with get_connection() as conn:
		conn.execute("""
			UPDATE business
			SET premium = FALSE
			WHERE premium = TRUE AND premium_valid_until IS NOT NULL AND premium_valid_until < ?
		""", (hoje,))
	
def mostrar_business_by_id(business_id):
	with get_connection() as conn:
		business = conn.execute("SELECT * FROM business WHERE id = ?", (business_id,)).fetchone()
		if business and business[13] and business[14]:
			if business[14] < datetime.date.today():
				conn.execute("""
					UPDATE business SET premium = FALSE WHERE id = ?
				""", (business_id,))
				business = dict(business)  # converte para dict
				business["premium"] = False
		return business
		
def mostrar_businesses_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, nome, logo_path, added_at, by_user, premium FROM business WHERE by_user = ?", (user_id,))
	meusbusinesses = cur.fetchall()
	conn.close()
	return meusbusinesses


def add_premium(premium, business_id, dias=None):
	with get_connection() as conn:
		if dias:
			valid_until = (datetime.date.today() + datetime.timedelta(days=dias))
		else:
			valid_until = None  # para assinatura recorrente

		conn.execute("""
			UPDATE business
			SET premium = ?,
				premium_valid_until = ?
			WHERE id = ?
		""", (premium, valid_until, business_id))