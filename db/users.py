from .connection import get_connection

def registrar_user(username, email, hashed, telephone):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute(
		"INSERT INTO users (username, email, password, telephone, descricao, pfp_filename) VALUES (%s, %s, %s, %s, %s, %s)",
		(username, email, hashed, telephone, None, None)
	)
	conn.commit()
	conn.close()


def edit_user(username, descricao, pfp_filename, user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		UPDATE users
		SET username = %s, descricao = %s, pfp_filename = %s
		WHERE id = %s
	""", (username, descricao, pfp_filename, user_id))
	conn.commit()
	conn.close()


def del_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
	conn.commit()
	conn.close()


def mostrar_user(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		SELECT id, username, role, joined_at, email, pfp_filename, descricao
		FROM users
		WHERE id = %s
	""", (user_id,))
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
	cur.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
	user = cur.fetchone()
	conn.close()
	return user


def tornar_admin(user_id):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("UPDATE users SET role = 'admin' WHERE id = %s", (user_id,))
	conn.commit()
	conn.close()