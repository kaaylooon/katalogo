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
		adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', None, 1, None)

		adicionar_business('Café & Prosa', 'O Café & Prosa é muito mais do que um café — é um ponto de encontro para quem ama cultura e boa conversa. Aqui você encontra cafés artesanais feitos com grãos selecionados, bolos e lanches fresquinhos, tudo preparado com carinho. Mas o diferencial vai além do cardápio: promovemos eventos culturais semanais, como leituras de poesia, workshops de escrita criativa, pequenos shows e encontros literários. Nosso espaço foi pensado para que cada visita seja uma experiência acolhedora, onde você pode relaxar, se inspirar e se conectar com outras pessoas que compartilham da paixão pela cultura.', 'Arte e Cultura', None, 1, 'Feira do Empreendedor')

		adicionar_business('Livraria Saber', 'A Livraria Saber é um espaço dedicado aos amantes da leitura, oferecendo uma vasta coleção de livros de todos os gêneros. Além das prateleiras recheadas de títulos, realizamos encontros literários, clubes de leitura e lançamentos de autores locais, criando um ambiente cultural ativo e inspirador.', 'Arte e Cultura', None, 1, None)

		adicionar_business('Ateliê das Cores', 'No Ateliê das Cores você encontra oficinas de pintura, desenho e artesanato, conduzidas por artistas experientes. Nosso objetivo é estimular a criatividade e oferecer um espaço de aprendizado e expressão para todas as idades. Organizamos exposições periódicas para que nossos alunos possam mostrar seus trabalhos.', 'Arte e Cultura', None, 1, None)

		adicionar_business('Cozinha Experimental', 'A Cozinha Experimental é um espaço onde gastronomia e criatividade se encontram. Oferecemos workshops de culinária, degustações temáticas e eventos gastronômicos, sempre com ingredientes frescos e técnicas inovadoras. É o lugar perfeito para quem ama cozinhar e experimentar novos sabores.', 'Gastronomia', None, 1, None)

		adicionar_business('Estúdio Harmonia', 'O Estúdio Harmonia oferece aulas de música, canto e produção musical, atendendo desde iniciantes até músicos avançados. Promovemos apresentações mensais e eventos colaborativos para que nossos alunos vivenciem a música em sua forma mais completa e compartilhada.', 'Música', None, 1, None)

		adicionar_business('Espaço Zen', 'O Espaço Zen é um refúgio para quem busca bem-estar e equilíbrio. Oferecemos aulas de yoga, meditação e terapias alternativas, além de workshops sobre hábitos saudáveis e desenvolvimento pessoal. Nosso objetivo é criar um ambiente acolhedor que promova saúde física e mental.', 'Bem-estar', None, 1, None)

		for business_id in range(1, 8):
				for dia_semana in range(7):
					add_horario(business_id, dia_semana, "08:00", "18:00")
	else:
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