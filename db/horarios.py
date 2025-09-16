from .connection import get_connection
import datetime
import sqlite3

def mostrar_disponivel(business_id):
	conn = get_connection()
	cur = conn.cursor()
	hoje = datetime.datetime.now().weekday()
	hoje = (hoje + 1)%7

	cur.execute("SELECT * FROM horarios WHERE business_id = ? AND dia_semana = ?", (business_id, hoje))

	horario = cur.fetchall()

	conn.close()
	return horario

def add_horario(business_id, dia_semana, abre, fecha):
	conn = get_connection()
	cur = conn.cursor()

	cur.execute("INSERT INTO horarios (business_id, dia_semana, abre, fecha) VALUES (?, ?, ?, ?)", (business_id, dia_semana, abre, fecha))
	conn.commit()
	conn.close()

def update_horario(business_id, dia_semana, abre, fecha):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE horarios 
        SET abre = ?, fecha = ?
        WHERE business_id = ? AND dia_semana = ?
    """, (abre, fecha, business_id, dia_semana))
    conn.commit()
    updated_rows = cur.rowcount
    conn.close()
    return updated_rows