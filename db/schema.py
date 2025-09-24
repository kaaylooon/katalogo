from .connection import get_connection
from db.users import tornar_admin, registrar_user
from db.business import adicionar_business, edit_business, add_premium
from db.horarios import add_horario
from db.images import add_business_images
from werkzeug.security import generate_password_hash
from services.logger import logger

def tabela_feed():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS feed (
			id SERIAL PRIMARY KEY,
			business_id INTEGER,
			description TEXT NOT NULL,
			by_user INTEGER,
			image_path TEXT,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	""")
	conn.commit()
	cur.close()
	conn.close()

def tabela_users():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY,
			username TEXT NOT NULL,
			email TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL,
			telephone TEXT NOT NULL,
			pfp_filename TEXT DEFAULT NULL,
			role TEXT NOT NULL DEFAULT 'user',
			joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			descricao TEXT
		)
	""")
	conn.commit()
	cur.close()
	conn.close()

def tabela_business():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS business (
			id SERIAL PRIMARY KEY,
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
			evento TEXT,
			address TEXT,
			integrantes TEXT,
			FOREIGN KEY (by_user) REFERENCES users(id) ON DELETE SET NULL

		)
	""")
	conn.commit()
	cur.close()
	conn.close()

def tabela_comentarios():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS comentarios (
			id SERIAL PRIMARY KEY,
			user_id INTEGER,
			content TEXT,
			business_id INTEGER,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			edited BOOLEAN DEFAULT FALSE,
			FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
			FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE

		)
	""")
	conn.commit()
	cur.close()
	conn.close()

def tabela_horarios():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS horarios (
			id SERIAL PRIMARY KEY,
			business_id INTEGER NOT NULL,
			dia_semana INTEGER NOT NULL,
			abre TIME NOT NULL,
			fecha TIME NOT NULL,
			FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
		)
	""")
	conn.commit()
	cur.close()
	conn.close()

def business_images_table():
	conn = get_connection()
	cur = conn.cursor()
	cur.execute("""
		CREATE TABLE IF NOT EXISTS business_images (
			id SERIAL PRIMARY KEY,
			business_id INTEGER NOT NULL,
			image_filename TEXT NOT NULL,
			FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
		)
	""")
	conn.commit()
	cur.close()
	conn.close()


def seed_db(full):
	conn = get_connection()
	cur = conn.cursor()
	hashed = generate_password_hash("adm545!7")
	cur.execute("""
		INSERT INTO users (id, username, email, password, telephone, role)
		VALUES (%s, %s, %s, %s, %s, %s)
		ON CONFLICT (id) DO NOTHING
	""", (1, "Someone", "kaylon.contact@outlook.com", hashed, "(11) 91659-1346", "admin"))
	conn.commit()
	cur.close()
	conn.close()

	if full:
		try:
			business_id = adicionar_business(
				'Aurum Initium',
				'Um curso voltado para construir uma base sólida em Matemática e Física...',
				'Livros e Educação',
				'@auriuminitium',
				'',
				'',
				1,
				'Feira do Empreendedor'
			)
			add_premium(True, business_id)
			edit_business(business_id, instagram='@auriuminitium', numero='(11) 91659-1346',
						  email='kaylon.contact@gmail.com', logo_path=None, lat=-12.1358, lon=-40.36,
						  address="Rua Planalto, 405, Macajuba - BA, Brasil")
			for dia_semana in range(7):
				add_horario(business_id, dia_semana, "08:00", "18:00")
		except Exception as e:
			logger.exception("Erro ao popular DB...")

def init_db():
	tabela_feed()
	tabela_users()
	tabela_business()
	tabela_comentarios()
	tabela_horarios()
	business_images_table()
