from .connection import get_connection
import datetime
import psycopg2.extras

def mostrar_disponivel(business_id):
	conn = get_connection()
	hoje = (datetime.datetime.now().weekday() + 1) % 7
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""
		SELECT * 
		FROM horarios 
		WHERE business_id = %s AND dia_semana = %s
	""", (business_id, hoje))
	rows = cur.fetchall()
	conn.close()
	return [dict(r) for r in rows]  # cada row vira dict automaticamente


def add_horario(business_id, dia_semana, abre, fecha):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""
		INSERT INTO horarios (business_id, dia_semana, abre, fecha) 
		VALUES (%s, %s, %s, %s)
	""", (business_id, dia_semana, abre, fecha))
	conn.commit()
	conn.close()

def del_horario(business_id, dias_num):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	try:
		cur.execute("DELETE FROM horarios WHERE business_id = %s AND dias_num = %s",
					(business_id, dias_num))
		conn.commit()
	except Exception as e:
		conn.rollback()
		print(f"Erro ao deletar horário: {e}")
	finally:
		cur.close()
		conn.close()



def update_horario(business_id, dia_semana, abre, fecha):
	conn = get_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""
		UPDATE horarios 
		SET abre = %s, fecha = %s
		WHERE business_id = %s AND dia_semana = %s
	""", (abre, fecha, business_id, dia_semana))
	updated_rows = cur.rowcount
	conn.commit()
	conn.close()
	return updated_rows
