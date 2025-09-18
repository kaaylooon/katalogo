import datetime
import sqlite3
from .connection import get_connection

def add_comentario(user_id, business_id, 
		content):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO comentarios (user_id, business_id, content) VALUES (?, ?, ?)", (user_id,
		business_id, content))

	cur.execute("UPDATE business SET comments_count = comments_count + 1 WHERE id = ?", (business_id,))

	conn.commit()
	conn.close()

def del_comentario(comment_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM comentarios WHERE id =?", (comment_id,))
	conn.commit()
	conn.close()

def mostrar_comentarios_business(business_id):
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

def mostrar_comentarios():
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()

	cur.execute("""
		SELECT c.*, u.username, u.pfp_path
		FROM comentarios c 
		JOIN users u ON c.user_id = u.id
		JOIN business b ON c.business_id = b.id
		ORDER BY c.created_at DESC
	""")

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

def mostrar_comentario_by_id(comment_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, user_id, business_id, content, created_at, edited FROM comentarios WHERE id = ?", (comment_id,))
	row = cur.fetchone()
	conn.close()
	if not row:
		return None
	return {
		"id": row[0],
		"user_id": row[1],
		"business_id": row[2],
		"content": row[3],
		"created_at": row[4],
		"edited": row[5]
	}

def comentar():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("UPDATE feed SET comments_count = comments_count + 1")
	conn.commit()
	conn.close()

def editar_comentario(content, edited, comment_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		UPDATE comentarios
		SET content = ?, edited = ?
		WHERE id = ?
	""", (content, edited, comment_id))
	conn.commit()
	conn.close()