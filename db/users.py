from .connection import get_connection

def registrar_user(username, email, hashed, telephone):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO users (username, email, password, telephone, descricao) VALUES (?, ?, ?, ?, ?)", (username, email, hashed, telephone, ''))
	conn.commit()
	conn.close()


def edit_user(username, descricao, user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		UPDATE users
		SET username = ?, descricao = ?
		WHERE id = ?
	""", (username, descricao, user_id))
	conn.commit()
	conn.close()


def mostrar_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("SELECT id, username, role, joined_at, email, pfp_path FROM users WHERE id = ?", (user_id,))
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