from .connection import get_connection

def mostrar_feed():
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT f.*, b.nome, b.logo_path, b.comments_count
			FROM feed f
			JOIN business b ON f.business_id = b.id
			ORDER BY f.created_at DESC
		""")
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		feed = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return feed

def mostrar_feed_business(business_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			SELECT f.*, b.nome, b.logo_path, b.comments_count
			FROM feed f
			JOIN business b ON f.business_id = b.id
			WHERE f.business_id = %s
			ORDER BY f.created_at DESC
		""", (business_id,))
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		feeds = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return feeds

def mostrar_feed_by_id(feed_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM feed WHERE id = %s", (feed_id,))
		row = cur.fetchone()
		if not row:
			return None
		colnames = [desc[0] for desc in cur.description]
		feed = dict(zip(colnames, row))
	conn.close()
	return feed

def add_feed(business_id, description, by_user, image_path):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO feed (business_id, description, by_user, image_path)
			VALUES (%s, %s, %s, %s)
			ON CONFLICT DO NOTHING
		""", (business_id, description, by_user, image_path))
	conn.commit()
	conn.close()

def del_feed(feed_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("DELETE FROM feed WHERE id = %s", (feed_id,))
	conn.commit()
	conn.close()
