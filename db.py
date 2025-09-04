import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "db.db")

#FEED

def tabela_feed():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS feed (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		description TEXT NOT NULL,
		category TEXT,
		contact TEXT,
		image_path TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	conn.close()

def mostrar_feed():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM feed ORDER BY created_at DESC")
	feed = cur.fetchall()
	conn.close()
	return feed

#USERS

def tabela_users():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT NOT NULL,
		email TEXT NOT NULL,
		password TEXT,
		telephone TEXT,
		pfp_path TEXT,
		joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	conn.close()

def mostrar_users():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM users ORDER BY joined_at DESC")
	users = cur.fetchall()
	conn.close()
	return users

#BUSINESS

def tabela_business():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS business (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nome TEXT NOT NULL,
		descricao TEXT,
		categoria TEXT,
		contato TEXT,
		logo_path TEXT,
		added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	conn.close()

def mostrar_business():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM business ORDER BY added_at DESC")
	business = cur.fetchall()
	conn.close()
	return business

def buscar_business(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM business WHERE id = ?", (business_id,))
	business = cur.fetchone()
	conn.close()
	return business

def adicionar_business(nome, descricao, categoria, contato, filename):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT INTO business (nome, descricao, categoria, contato, logo_path) VALUES (?, ?, ?, ?, ?)", (nome, descricao, categoria, contato, filename))
	conn.commit()
	conn.close()



#INIT

def init_db():
	tabela_feed()
	tabela_users()
	tabela_business()
