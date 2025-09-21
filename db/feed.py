from .connection import get_connection
import psycopg2.extras

def mostrar_feed():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT f.*, b.nome, b.logo_path, b.comments_count
        FROM feed f
        JOIN business b ON f.business_id = b.id
        ORDER BY f.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mostrar_feed_business(business_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT f.*, b.nome, b.logo_path, b.comments_count
        FROM feed f
        JOIN business b ON f.business_id = b.id
        WHERE f.business_id = %s
        ORDER BY f.created_at DESC
    """, (business_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mostrar_feed_by_id(feed_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM feed WHERE id = %s", (feed_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def add_feed(business_id, description, by_user, image_path):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        INSERT INTO feed (business_id, description, by_user, image_path)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (business_id, description, by_user, image_path))
    conn.commit()
    conn.close()


def del_feed(feed_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM feed WHERE id = %s", (feed_id,))
    conn.commit()
    conn.close()
