from .connection import get_connection
import psycopg2.extras

def add_notification_db(user_id, message):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""
		INSERT INTO notifications (user_id, message)
		VALUES (%s, %s)
	""", (user_id, message))
	conn.commit()
	conn.close()
	cur.close()

def get_user_notifications(user_id, limit=50):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""
		SELECT * FROM notifications 
		WHERE user_id=%s 
		ORDER BY created_at DESC 
		LIMIT %s
	""", (user_id, limit))
	notifications = cur.fetchall()  # <- retorna lista de dicts
	cur.close()
	conn.close()
	return notifications
