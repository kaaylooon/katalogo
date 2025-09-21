from .connection import get_connection
import psycopg2.extras

def add_business_images(business_id, image_filename):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "INSERT INTO business_images (business_id, image_filename) VALUES (%s, %s)",
        (business_id, image_filename)
    )
    conn.commit()
    conn.close()


def delete_business_image(business_id, image_filename):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "DELETE FROM business_images WHERE business_id = %s AND image_filename = %s",
        (business_id, image_filename)
    )
    conn.commit()
    conn.close()


def mostrar_business_images_urls(business_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT * FROM business_images WHERE business_id = %s",
        (business_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]  # cada row já vira dict automaticamente
