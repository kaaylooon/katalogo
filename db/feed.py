import sqlite3
from .connection import get_connection

def mostrar_feed():
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("""
		SELECT f.*, b.nome, b.logo_path, b.comments_count
		FROM feed f
		JOIN business b ON f.business_id = b.id
		ORDER BY f.created_at DESC
	""")
	feed = cur.fetchall()
	conn.close()
	return feed

def mostrar_feed_business(business_id):
	conn = get_connection()
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("""
		SELECT f.*, b.nome, b.logo_path, b.comments_count
		FROM feed f
		JOIN business b ON f.business_id = b.id
		WHERE f.business_id = ?
		ORDER BY f.created_at DESC
	""", (business_id,))
	feeds = cur.fetchall()
	conn.close()
	return feeds

def add_feed(business_id, description, by_user, image_path):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT OR IGNORE INTO feed (business_id,description, by_user, image_path) VALUES (?, ?, ?, ?)", (business_id, description, by_user, image_path))
	conn.commit()
	conn.close()