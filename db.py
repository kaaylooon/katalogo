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
		by_user TEXT,
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
		username TEXT NOT NULL UNIQUE,
		email TEXT NOT NULL UNIQUE,
		password TEXT NOT NULL,
		telephone TEXT NOT NULL,
		pfp_path TEXT,
		role TEXT NOT NULL DEFAULT 'user',
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

def mostrar_user(user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT id, username, role, joined_at, email, pfp_path FROM users WHERE id = ?", (user_id,))
	user_dados = cur.fetchone()
	conn.close()
	return user_dados

def mostrar_businesses_user(user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT id, nome, logo_path, added_at, by_user FROM business WHERE by_user = ?", (user_id,))
	meusbusinesses = cur.fetchall()
	conn.close()
	return meusbusinesses

def registrar_user(username, email, hashed, telephone):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT OR IGNORE INTO users (username, email, password, telephone) VALUES (?, ?, ?, ?)", (username, email, hashed, telephone))
	conn.commit()
	conn.close()

def verificar_user(username):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
	user = cur.fetchone()
	conn.close()
	return user

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
		added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		by_user TEXT
		)
	""")
	conn.commit()
	conn.close()

def mostrar_business(search_query):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	if search_query:
		cur.execute("SELECT * FROM business WHERE nome LIKE ? ORDER BY added_at DESC", ('%' + search_query + '%',))
	else:
		cur.execute("SELECT * FROM business ORDER BY added_at DESC")
	businesses = cur.fetchall()
	conn.close()
	return businesses

def buscar_id_business(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM business WHERE id = ?", (business_id,))
	business = cur.fetchone()
	conn.close()
	return business

def buscar_nome_business(nome):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT id FROM business WHERE nome = ?", (nome,))
	business = cur.fetchone()
	conn.close()
	return business[0] if business else None

def adicionar_business(nome, descricao, categoria, contato, filename, by_user):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT INTO business (nome, descricao, categoria, contato, logo_path, by_user) VALUES (?, ?, ?, ?, ?, ?)", (nome, descricao, categoria, contato, filename, by_user))
	conn.commit()
	conn.close()

#MISC

def tornar_admin(user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
	conn.commit()
	conn.close()

#INIT

def init_db():
	tabela_feed()
	tabela_users()
	tabela_business()

	tornar_admin(1)
	#tornar_admin(2)
