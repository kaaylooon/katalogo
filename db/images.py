from .connection import get_connection

def add_business_images(business_id, image_filename):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute(
			"INSERT INTO business_images (business_id, image_filename) VALUES (%s, %s)",
			(business_id, image_filename)
		)
	conn.commit()
	conn.close()

def delete_business_image(business_id, image_filename):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute(
			"DELETE FROM business_images WHERE image_filename = %s",
			(image_filename,)
		)
	conn.commit()
	conn.close()

def mostrar_business_images_urls(business_id):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute(
			"SELECT * FROM business_images WHERE business_id = %s",
			(business_id,)
		)
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		result = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return result
