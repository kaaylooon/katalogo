import sqlite3
from .connection import get_connection

def add_comentario(user_id,
		content, business_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO comentarios (user_id, content, business_id) VALUES (?, ?, ?)", (user_id,
		content, business_id))

	cur.execute("UPDATE business SET comments_count = comments_count + 1 WHERE id = ?", (business_id,))

	conn.commit()
	conn.close()


def mostrar_comentarios(business_id):
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()

	cur.execute("""
		SELECT c.*, u.username, u.pfp_path
		FROM comentarios c 
		JOIN users u ON c.user_id = u.id
		JOIN business b ON c.business_id = b.id
		WHERE c.business_id = ?
		ORDER BY c.created_at DESC
	""", (business_id,))

	comentarios = cur.fetchall()
	conn.close()
	return comentarios

def mostrar_comentarios_user(user_id):
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()

	cur.execute("""
		SELECT c.*, u.username, u.pfp_path
		FROM comentarios c 
		JOIN users u ON c.user_id = u.id
		JOIN business b ON c.business_id = b.id
		WHERE c.user_id = ?
		ORDER BY c.created_at DESC
	""", (user_id,))

	comentarios = cur.fetchall()
	conn.close()
	return comentarios


def comentar():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute()

	cur.execute("UPDATE feed SET comments_count = comments_count + 1")
