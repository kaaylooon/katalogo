from .connection import get_connection

def add_business_images(business_id, image_filename):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("INSERT INTO business_images (business_id, image_filename) VALUES (?, ?)", (business_id, image_filename))
	conn.commit()
	conn.close()

def delete_business_image(business_id, image_filename):
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("DELETE FROM business_images WHERE image_filename=?", (image_filename,))
	conn.commit()
	conn.close()

def mostrar_business_images_urls(business_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM business_images WHERE business_id = ?", (business_id,))
    rows = cur.fetchall()
    conn.close()
    return [{'id': r[0], 'business_id': r[1], 'image_path': r[2]} for r in rows]
