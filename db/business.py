import psycopg2
from psycopg2.extras import DictCursor
from .connection import get_connection
import datetime

def adicionar_business(nome, descricao, categoria, instagram, numero, filename, by_user, evento, integrantes=None):
    conn = get_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            INSERT INTO business (nome, descricao, categoria, instagram, numero, email, logo_path, by_user, lat, lon, evento, integrantes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (nome, descricao, categoria, instagram, numero, '', filename, by_user, None, None, evento, integrantes))
        business_id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return business_id

def edit_business(business_id, **kwargs):
    allowed_fields = ['nome', 'categoria', 'descricao', 'instagram', 'numero', 'email', 'logo_path', 'lat', 'lon', 'address']
    set_clause = []
    params = []

    for field in allowed_fields:
        if field in kwargs and kwargs[field] not in [None, '']:
            set_clause.append(f"{field} = %s")
            params.append(kwargs[field])

    if not set_clause:
        return  # nada pra atualizar

    params.append(business_id)
    query = f"UPDATE business SET {', '.join(set_clause)} WHERE id = %s"

    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, tuple(params))
    conn.commit()
    conn.close()

def del_business(business_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM business WHERE id = %s", (business_id,))
    conn.commit()
    conn.close()

def buscar_id_business(business_id):
    conn = get_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("SELECT * FROM business WHERE id = %s", (business_id,))
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def mostrar_business(search_query='', categoria=''):
    conn = get_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        query = "SELECT * FROM business WHERE 1=1"
        params = []

        if search_query:
            query += " AND nome ILIKE %s"
            params.append(f"%{search_query}%")
        if categoria:
            query += " AND categoria = %s"
            params.append(categoria)

        query += " ORDER BY premium DESC, added_at DESC"
        cur.execute(query, params)
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def buscar_nome_business(nome):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM business WHERE nome = %s", (nome,))
        row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def desativar_premium_expirado():
    hoje = datetime.date.today()
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE business
            SET premium = FALSE
            WHERE premium = TRUE AND premium_valid_until IS NOT NULL AND premium_valid_until < %s
        """, (hoje,))
    conn.commit()
    conn.close()

def mostrar_business_by_id(business_id):
    conn = get_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("SELECT * FROM business WHERE id = %s", (business_id,))
        row = cur.fetchone()
        if row:
            business = dict(row)
            if business.get('premium') and business.get('premium_valid_until') and business['premium_valid_until'] < datetime.date.today():
                cur.execute("UPDATE business SET premium = FALSE WHERE id = %s", (business_id,))
                conn.commit()
                business['premium'] = False
        else:
            business = None
    conn.close()
    return business

def mostrar_businesses_user(user_id):
    conn = get_connection()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT id, nome, logo_path, added_at, by_user, premium 
            FROM business 
            WHERE by_user = %s
        """, (user_id,))
        rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_premium(premium, business_id, dias=None):
    valid_until = (datetime.date.today() + datetime.timedelta(days=dias)) if dias else None
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE business
            SET premium = %s,
                premium_valid_until = %s
            WHERE id = %s
        """, (premium, valid_until, business_id))
    conn.commit()
    conn.close()
