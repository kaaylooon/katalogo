from .connection import get_connection
import psycopg2.extras

def registrar_user(username, email, hashed, telephone):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "INSERT INTO users (username, email, password, telephone, descricao, pfp_filename) VALUES (%s, %s, %s, %s, %s, %s)",
        (username, email, hashed, telephone, None, None)
    )
    conn.commit()
    conn.close()


def edit_user(username, descricao, pfp_filename, user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        UPDATE users
        SET username = %s, descricao = %s, pfp_filename = %s
        WHERE id = %s
    """, (username, descricao, pfp_filename, user_id))
    conn.commit()
    conn.close()


def del_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()


def mostrar_user(user_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT id, username, role, joined_at, email, pfp_filename, descricao
        FROM users
        WHERE id = %s
    """, (user_id,))
    user_dados = cur.fetchone()  # agora é um DictRow
    conn.close()
    return dict(user_dados) if user_dados else None


def mostrar_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM users ORDER BY joined_at DESC")
    users = cur.fetchall()
    conn.close()
    return [dict(u) for u in users]  # converte cada row em dict


def verificar_user(username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    conn.close()
    return dict(user) if user else None


def tornar_admin(username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("UPDATE users SET role = 'admin' WHERE username = %s", (username,))
    conn.commit()
    conn.close()
