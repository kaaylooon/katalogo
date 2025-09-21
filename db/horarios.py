from .connection import get_connection
import datetime

def mostrar_disponivel(business_id):
	conn = get_connection()
	hoje = (datetime.datetime.now().weekday() + 1) % 7
	with conn.cursor() as cur:
		cur.execute("""
			SELECT * 
			FROM horarios 
			WHERE business_id = %s AND dia_semana = %s
		""", (business_id, hoje))
		rows = cur.fetchall()
		colnames = [desc[0] for desc in cur.description]
		horario = [dict(zip(colnames, r)) for r in rows]
	conn.close()
	return horario

def add_horario(business_id, dia_semana, abre, fecha):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO horarios (business_id, dia_semana, abre, fecha) 
			VALUES (%s, %s, %s, %s)
		""", (business_id, dia_semana, abre, fecha))
	conn.commit()
	conn.close()

def update_horario(business_id, dia_semana, abre, fecha):
	conn = get_connection()
	with conn.cursor() as cur:
		cur.execute("""
			UPDATE horarios 
			SET abre = %s, fecha = %s
			WHERE business_id = %s AND dia_semana = %s
		""", (abre, fecha, business_id, dia_semana))
		updated_rows = cur.rowcount
	conn.commit()
	conn.close()
	return updated_rows
