from .connection import get_connection

def add_comentario(user_id, business_id, content):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO comentarios (user_id, business_id, content)
			VALUES (%s, %s, %s)
		""", (user_id, business_id, content))

		cur.execute("UPDATE business SET comments_count = comments_count + 1 WHERE id = %s", (business_id,))
	conn.commit()
	conn.close()

def del_comentario(comment_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("DELETE FROM comentarios WHERE id = %s", (comment_id,))
	conn.commit()
	conn.close()

def mostrar_comentarios_business(business_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT c.*, u.username, u.pfp_filename
			FROM comentarios c 
			JOIN users u ON c.user_id = u.id
			JOIN business b ON c.business_id = b.id
			WHERE c.business_id = %s
			ORDER BY c.created_at DESC
		""", (business_id,))
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		comentarios = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return comentarios

def mostrar_comentarios():
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT c.*, u.username, u.pfp_filename
			FROM comentarios c 
			JOIN users u ON c.user_id = u.id
			JOIN business b ON c.business_id = b.id
			ORDER BY c.created_at DESC
		""")
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		comentarios = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return comentarios

def mostrar_comentarios_user(user_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT c.*, u.username, u.pfp_filename
			FROM comentarios c 
			JOIN users u ON c.user_id = u.id
			JOIN business b ON c.business_id = b.id
			WHERE c.user_id = %s
			ORDER BY c.created_at DESC
		""", (user_id,))
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		comentarios = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return comentarios

def mostrar_comentario_by_id(comment_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT id, user_id, business_id, content, created_at, edited
			FROM comentarios
			WHERE id = %s
		""", (comment_id,))
		row = cur.fetchone()
		if not row:
			return None
		colnames = [desc[0] for desc in cur.description]
		comentario = dict(zip(colnames, row))
	conn.close()
	return comentario

def comentar():
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("UPDATE feed SET comments_count = comments_count + 1")
	conn.commit()
	conn.close()

def editar_comentario(content, edited, comment_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			UPDATE comentarios
			SET content = %s, edited = %s
			WHERE id = %s
		""", (content, edited, comment_id))
	conn.commit()
	conn.close()
