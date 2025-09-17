from .connection import get_connection

from db.users import tornar_admin, registrar_user
from db.business import adicionar_business, edit_business, add_premium
from db.horarios import add_horario
from db.images import add_business_images

from werkzeug.security import generate_password_hash

def tabela_feed():
	with get_connection() as conn:
		conn.execute("""
			CREATE TABLE IF NOT EXISTS feed (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				business_id TEXT,
				description TEXT NOT NULL,
				by_user TEXT,
				image_path TEXT,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			)
		""")

def tabela_users():
	with get_connection() as conn:
		conn.execute("""
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

def tabela_business():
	with get_connection() as conn:
		conn.execute("""
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

def tabela_comentarios():
	with get_connection() as conn:
		conn.execute("""
			CREATE TABLE IF NOT EXISTS comentarios (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER,
				content TEXT,
				business_id INTEGER,
				created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
			)
		""")

def tabela_horarios():
	with get_connection() as conn:
		conn.execute("""
			CREATE TABLE IF NOT EXISTS horarios (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				business_id INTEGER NOT NULL,
				dia_semana INTEGER NOT NULL,
				abre TIME NOT NULL,
				fecha TIME NOT NULL,
				FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
			)
		""")

def business_images_table():
	with get_connection() as conn:
		conn.execute("""
			CREATE TABLE IF NOT EXISTS business_images (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				business_id INTEGER NOT NULL,
				image_filename TEXT NOT NULL,
				FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
			)
		""")

def seed_db(full):

	registrar_user('Kaylon', 'kaylon.contact@outlook.com', generate_password_hash('adm123'), '(11) 12345-6789')

	tornar_admin(1)

	if full:
		adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', None, 1, 'Feira do Empreendedor')

		add_premium(True, 1)

		edit_business(1, instagram='@auriuminitium', numero='(11) 91659-1346', email='kaylon.contact@gmail.com', logo_path='7560eb2c5c984d66b0a02e6e07d9a8fa.jpeg', lat=-12.1358, lon=-40.36)

		add_business_images(1, '7560eb2c5c984d66b0a02e6e07d9a8fa.jpeg')

		for dia_semana in range(7): add_horario(1, dia_semana, "08:00", "18:00")

		adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', None, 1, 'Feira do Empreendedor')

		edit_business(2, instagram='@auriuminitium', numero='(11) 91659-1346', email='kaylon.contact@gmail.com', logo_path='7560eb2c5c984d66b0a02e6e07d9a8fa.jpeg', lat=-12.1358, lon=-40.36)

		add_business_images(2, '7560eb2c5c984d66b0a02e6e07d9a8fa.jpeg')

		for dia_semana in range(7): add_horario(2, dia_semana, "08:00", "18:00")


def init_db():
	tabela_feed()
	tabela_users()
	tabela_business()
	tabela_comentarios()
	tabela_horarios()
	business_images_table()