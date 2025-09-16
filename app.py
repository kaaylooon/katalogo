from flask import Flask
from werkzeug.security import generate_password_hash

import arrow

from routes import routes
from auth import auth

from db import init_db, tornar_admin, registrar_user, adicionar_business, add_feed, add_horario

app = Flask(__name__)

app.secret_key = "secret_key"

app.register_blueprint(routes) 
app.register_blueprint(auth) 

def humanize_datetime(value):
		return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

push = True

if push:
	init_db()

	registrar_user('Kaylon', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 12345-6789')

	tornar_admin(1)

	#adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', '@auruminitium', '(11) 91659-1346', 'kaylon.alt@outlook.com', 'auriuminitium.jpeg', 1, -12.1358, -40.36)

	adicionar_business('Café & Prosa', 'O Café & Prosa é muito mais do que um café — é um ponto de encontro para quem ama cultura e boa conversa. Aqui você encontra cafés artesanais feitos com grãos selecionados, bolos e lanches fresquinhos, tudo preparado com carinho. Mas o diferencial vai além do cardápio: promovemos eventos culturais semanais, como leituras de poesia, workshops de escrita criativa, pequenos shows e encontros literários. Nosso espaço foi pensado para que cada visita seja uma experiência acolhedora, onde você pode relaxar, se inspirar e se conectar com outras pessoas que compartilham da paixão pela cultura.', 'Arte e Cultura', None, 1, None)

	adicionar_business('Livraria Saber', 'A Livraria Saber é um espaço dedicado aos amantes da leitura, oferecendo uma vasta coleção de livros de todos os gêneros. Além das prateleiras recheadas de títulos, realizamos encontros literários, clubes de leitura e lançamentos de autores locais, criando um ambiente cultural ativo e inspirador.', 'Arte e Cultura', None, 1, None)

	adicionar_business('Ateliê das Cores', 'No Ateliê das Cores você encontra oficinas de pintura, desenho e artesanato, conduzidas por artistas experientes. Nosso objetivo é estimular a criatividade e oferecer um espaço de aprendizado e expressão para todas as idades. Organizamos exposições periódicas para que nossos alunos possam mostrar seus trabalhos.', 'Arte e Cultura', None, 1, None)

	adicionar_business('Cozinha Experimental', 'A Cozinha Experimental é um espaço onde gastronomia e criatividade se encontram. Oferecemos workshops de culinária, degustações temáticas e eventos gastronômicos, sempre com ingredientes frescos e técnicas inovadoras. É o lugar perfeito para quem ama cozinhar e experimentar novos sabores.', 'Gastronomia', None, 1, None)

	adicionar_business('Estúdio Harmonia', 'O Estúdio Harmonia oferece aulas de música, canto e produção musical, atendendo desde iniciantes até músicos avançados. Promovemos apresentações mensais e eventos colaborativos para que nossos alunos vivenciem a música em sua forma mais completa e compartilhada.', 'Música', None, 1, None)

	adicionar_business('Espaço Zen', 'O Espaço Zen é um refúgio para quem busca bem-estar e equilíbrio. Oferecemos aulas de yoga, meditação e terapias alternativas, além de workshops sobre hábitos saudáveis e desenvolvimento pessoal. Nosso objetivo é criar um ambiente acolhedor que promova saúde física e mental.', 'Bem-estar', None, 1, None)

	for business_id in range(1, 11):
			for dia_semana in range(7):
				add_horario(business_id, dia_semana, "08:00", "18:00")
else:
	if __name__ == "__main__":
		init_db()

		registrar_user('Kaylon', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 12345-6789')

		tornar_admin(1)

		adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', None, 1, None)

		for business_id in range(1, 11):
				for dia_semana in range(7):
					add_horario(business_id, dia_semana, "08:00", "18:00")
		app.run(host="0.0.0.0", debug=True)
