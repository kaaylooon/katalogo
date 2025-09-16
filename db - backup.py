import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "db.db")

def tabela_feed():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS feed (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		business_id TEXT,
		description TEXT NOT NULL,
		by_user TEXT,
		image_path TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	conn.close()

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
		joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		descricao TEXT
		)
	""")
	conn.commit()
	conn.close()

def tabela_business():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS business (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nome TEXT NOT NULL,
		descricao TEXT,
		categoria TEXT,
		instagram TEXT,
		numero TEXT,
		email TEXT,
		logo_path TEXT,
		added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		by_user INTEGER,
		comments_count INTEGER DEFAULT 0,
		lat REAL, 
		lon REAL,
		premium BOOLEAN DEFAULT FALSE,
		premium_valid_until DATE,
		evento TEXT
		)
	""")
	conn.commit()
	conn.close()

def tabela_comentarios():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS comentarios (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		content TEXT,
		business_id INTEGER,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	conn.close()

def tabela_horarios():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS horarios(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			business_id INTEGER NOT NULL,
			dia_semana INTEGER NOT NULL,
			abre TIME NO NULL,
			fecha TIME NOT NULL,
			FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
		)
	""")

def business_images_table():
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS business_images(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			business_id INTEGER NOT NULL,
			image_url TEXT NOT NULL,
			FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
		)
	""")

def add_business_images(business_id, image_url):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT INTO business_images VALUES (business_id, image_url) VALUES (?, ?)", (business_id, image_url))
	conn.commit()
	conn.close()

def mostrar_business_images_urls(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM business_images WHERE business_id = ?", (business_id,))
	images_urls = cur.fetchall()
	return images_urls


def add_premium(premium, business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		UPDATE business
		SET premium = ?
		WHERE id = ?
	""", (premium, business_id))
	conn.commit()
	conn.close()


def edit_business(nome, categoria, descricao, instagram, numero, email, filename, business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		UPDATE business
		SET nome = ?, categoria = ?, descricao = ?, instagram = ?, numero = ?, email = ?, logo_path = ?
		WHERE id = ?
	""", (nome, categoria, descricao, instagram, numero, email, filename, business_id))
	conn.commit()
	conn.close()

def del_business(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("DELETE FROM business WHERE id = ?", (business_id,))
	conn.commit()
	conn.close()

def mostrar_disponivel(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	cur.execute("SELECT * FROM horarios WHERE business_id = ? AND dia_semana = strftime('%w', 'now', 'localtime')", (business_id,))

	horario = cur.fetchall()

	conn.close()
	return horario

def add_horario(business_id, dia_semana, abre, fecha):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	cur.execute("INSERT INTO horarios (business_id, dia_semana, abre, fecha) VALUES (?, ?, ?, ?)", (business_id, dia_semana, abre, fecha))
	conn.commit()
	conn.close()


def mostrar_comentarios(business_id):
	conn = sqlite3.connect(DB_NAME)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()

	cur.execute("""
		SELECT c.*, u.username, u.pfp_path
		FROM comentarios c 
		JOIN users u ON c.user_id = u.id
		JOIN business b ON c.business_id = b.id
		WHERE c.business_id = ?
		ORDER BY c.created_at DESC
	""", (business_id,))

	comentarios = cur.fetchall()
	conn.close()
	return comentarios

def mostrar_comentarios_user(user_id):
	conn = sqlite3.connect(DB_NAME)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()

	cur.execute("""
		SELECT c.*, u.username, u.pfp_path
		FROM comentarios c 
		JOIN users u ON c.user_id = u.id
		JOIN business b ON c.business_id = b.id
		WHERE c.user_id = ?
		ORDER BY c.created_at DESC
	""", (user_id,))

	comentarios = cur.fetchall()
	conn.close()
	return comentarios

def add_comentario(user_id,
		content, business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT INTO comentarios (user_id, content, business_id) VALUES (?, ?, ?)", (user_id,
		content, business_id))

	cur.execute("UPDATE business SET comments_count = comments_count + 1 WHERE id = ?", (business_id,))

	conn.commit()
	conn.close()

def mostrar_feed():
	conn = sqlite3.connect(DB_NAME)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("""
		SELECT f.*, b.nome, b.logo_path, b.comments_count
		FROM feed f
		JOIN business b ON f.business_id = b.id
		ORDER BY f.created_at DESC
	""")
	feed = cur.fetchall()
	conn.close()
	return feed

def mostrar_feed_business(business_id):
	conn = sqlite3.connect(DB_NAME)
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	cur.execute("""
		SELECT f.*, b.nome, b.logo_path, b.comments_count
		FROM feed f
		JOIN business b ON f.business_id = b.id
		WHERE f.business_id = ?
		ORDER BY f.created_at DESC
	""", (business_id,))
	feeds = cur.fetchall()
	conn.close()
	return feeds

def add_feed(business_id, description, by_user, image_path):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT OR IGNORE INTO feed (business_id,description, by_user, image_path) VALUES (?, ?, ?, ?)", (business_id, description, by_user, image_path))
	conn.commit()
	conn.close()

#USERS

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


def edit_user(username, descricao, user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("""
		UPDATE users
		SET username = ?, descricao = ?
		WHERE id = ?
	""", (username, descricao, user_id))
	conn.commit()
	conn.close()

def mostrar_businesses_user(user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT id, nome, logo_path, added_at, by_user FROM business WHERE by_user = ?", (user_id,))
	meusbusinesses = cur.fetchall()
	conn.close()
	return meusbusinesses

def mostrar_business_by_id(business_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("SELECT * FROM business WHERE id = ?", (business_id,))
	business = cur.fetchone()
	conn.close()
	return business


def registrar_user(username, email, hashed, telephone):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT OR IGNORE INTO users (username, email, password, telephone, descricao) VALUES (?, ?, ?, ?, ?)", (username, email, hashed, telephone, ''))
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

def mostrar_business(search_query='', categoria=''):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()

	query = "SELECT * FROM business WHERE 1=1"
	params = []

	if search_query:
		query += " AND nome LIKE ?"
		params.append(f"%{search_query}%")

	if categoria:
		query += " AND categoria = ?"
		params.append(categoria)

	query += " ORDER BY added_at DESC"

	cur.execute(query, params)
	businesses = cur.fetchall()

	conn.close()
	return businesses

def buscar_id_business(business_id):
	conn = sqlite3.connect(DB_NAME)
	conn.row_factory = sqlite3.Row
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

def adicionar_business(nome, descricao, categoria, filename, by_user, evento):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("INSERT INTO business (nome, descricao, categoria, instagram, numero, email, logo_path, by_user, lat, lon) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome, descricao, categoria, '', '', '', filename, by_user, '', '', evento))
	conn.commit()
	conn.close()

#MISC

def tornar_admin(user_id):
	conn = sqlite3.connect(DB_NAME)
	cur = conn.cursor()
	cur.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
	conn.commit()
	conn.close()

def comentar():
	conn = sqlite3.connect()
	cur = conn.cursor()
	cur.execute()

	cur.execute("UPDATE feed SET comments_count = comments_count + 1")

#INIT

def init_db():
	tabela_feed()
	tabela_users()
	tabela_business()
	tabela_comentarios()
	tabela_horarios()
	business_images_table()