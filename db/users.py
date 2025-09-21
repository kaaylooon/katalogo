from .connection import get_connection
import sqlite3

def registrar_user(username, email, hashed, telephone):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO users (username, email, password, telephone, descricao, pfp_filename) VALUES (?, ?, ?, ?, ?, ?)", (username, email, hashed, telephone, None, None))
	conn.commit()
	conn.close()


def edit_user(username, descricao, pfp_filename, user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		UPDATE users
		SET username = ?, descricao = ?, pfp_filename=?
		WHERE id = ?
	""", (username, descricao, pfp_filename, user_id))
	conn.commit()
	conn.close()


def del_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
	conn.commit()
	conn.close()


def mostrar_user(user_id):
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("SELECT id, username, role, joined_at, email, pfp_filename, descricao FROM users WHERE id = ?", (user_id,))
	user_dados = cur.fetchone()
	conn.close()
	return user_dados

def mostrar_users():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT * FROM users ORDER BY joined_at DESC")
	users = cur.fetchall()
	conn.close()
	return users

def verificar_user(username):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
	user = cur.fetchone()
	conn.close()
	return user

def tornar_admin(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
	conn.commit()
	conn.close()