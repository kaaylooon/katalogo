from .connection import get_connection
import psycopg2.extras

def add_comentario(user_id, business_id, content):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        INSERT INTO comentarios (user_id, business_id, content)
        VALUES (%s, %s, %s)
    """, (user_id, business_id, content))

    cur.execute("UPDATE business SET comments_count = comments_count + 1 WHERE id = %s", (business_id,))
    conn.commit()
    conn.close()


def del_comentario(comment_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM comentarios WHERE id = %s", (comment_id,))
    conn.commit()
    conn.close()


def mostrar_comentarios_business(business_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT c.*, u.username, u.pfp_filename
        FROM comentarios c 
        JOIN users u ON c.user_id = u.id
        WHERE c.business_id = %s
        ORDER BY c.created_at DESC
    """, (business_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mostrar_comentarios():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT c.*, u.username, u.pfp_filename
        FROM comentarios c 
        JOIN users u ON c.user_id = u.id
        ORDER BY c.created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mostrar_comentarios_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT c.*, u.username, u.pfp_filename
        FROM comentarios c 
        JOIN users u ON c.user_id = u.id
        WHERE c.user_id = %s
        ORDER BY c.created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mostrar_comentario_by_id(comment_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT id, user_id, business_id, content, created_at, edited
        FROM comentarios
        WHERE id = %s
    """, (comment_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def editar_comentario(content, edited, comment_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        UPDATE comentarios
        SET content = %s, edited = %s
        WHERE id = %s
    """, (content, edited, comment_id))
    conn.commit()
    conn.close()
