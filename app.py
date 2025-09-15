from flask import Flask
from werkzeug.security import generate_password_hash

import arrow

from routes import routes
from auth import auth

from db import init_db, tornar_admin, registrar_user, adicionar_business, add_feed, add_horario

app = Flask(__name__)

app.secret_key = "aEfGbhD"

app.register_blueprint(routes) 
app.register_blueprint(auth) 

def humanize_datetime(value):
		return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

x = True

if x:
	init_db()

	registrar_user('Kaylon', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 12345-6789')

	tornar_admin(1)

	#adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', '@auruminitium', '(11) 91659-1346', 'kaylon.alt@outlook.com', 'auriuminitium.jpeg', 1, -12.1358, -40.36)

	adicionar_business('Café & Prosa', 'O Café & Prosa é muito mais do que um café — é um ponto de encontro para quem ama cultura e boa conversa. Aqui você encontra cafés artesanais feitos com grãos selecionados, bolos e lanches fresquinhos, tudo preparado com carinho. Mas o diferencial vai além do cardápio: promovemos eventos culturais semanais, como leituras de poesia, workshops de escrita criativa, pequenos shows e encontros literários. Nosso espaço foi pensado para que cada visita seja uma experiência acolhedora, onde você pode relaxar, se inspirar e se conectar com outras pessoas que compartilham da paixão pela cultura.', 'Arte e Cultura', '@cafeprosa', '(74) 98765-4321', 'contato@cafeprosa.com', None, 1, -12.9714, -38.5014)

	adicionar_business('TechLab Kids', 'O TechLab Kids é um laboratório de tecnologia e aprendizado para crianças e adolescentes, criado para estimular a curiosidade e desenvolver habilidades do século XXI. Oferecemos cursos de programação, robótica, eletrônica, design digital e ciências de forma prática e divertida. Aqui, os alunos aprendem enquanto criam projetos reais, fortalecendo o raciocínio lógico, a criatividade e a capacidade de resolver problemas. Nosso objetivo é formar jovens inovadores e confiantes, preparados para um mundo cada vez mais tecnológico.', 'Tecnologia e Informática', '@techlabkids', '(21) 99876-5432', 'contato@techlabkids.com', None, 1, -12.9711, -38.5100)

	adicionar_business('Flor & Arte', 'A Flor & Arte é uma floricultura e loja de presentes que transforma cada flor em uma experiência única. Trabalhamos com arranjos personalizados, buquês temáticos e combinações de flores com objetos de decoração artesanal, perfeitas para presentear, decorar ambientes ou comemorar momentos especiais. Cada peça é criada com atenção aos detalhes, buscando harmonia entre cores, formas e significados. Mais do que vender flores, queremos oferecer emoções e memórias, tornando cada presente uma lembrança inesquecível.', 'Arte e Cultura', '@florearte', '(31) 91234-5678', 'contato@florearte.com', None, 1, -12.2677, -38.9667)

	adicionar_business('MoveFit Studio', 'O MoveFit Studio é uma academia boutique dedicada a transformar a experiência de treinar em algo único e personalizado. Oferecemos aulas de pilates, yoga, treino funcional e programas de musculação adaptados ao perfil de cada aluno. Nosso time de profissionais acompanha de perto a evolução de cada pessoa, ajudando a atingir objetivos de forma saudável e eficiente. Aqui, o treino vai além do físico — é uma jornada de autoconhecimento, disciplina e saúde mental, dentro de um ambiente acolhedor e motivador.', 'Saúde e Bem-estar', '@movefitstudio', '(41) 98765-2109', 'contato@movefitstudio.com', None, 1, -12.9784, -38.5110)

	adicionar_business('Doce Encanto', 'O Doce Encanto é uma confeitaria artesanal dedicada a criar doces que encantam pela aparência e pelo sabor. Nossa especialidade são bolos temáticos, sobremesas individuais e kits de doces para festas e eventos corporativos, todos produzidos com ingredientes selecionados e técnicas artesanais que garantem qualidade e frescor. Cada criação é cuidadosamente planejada para transmitir emoção e tornar momentos especiais ainda mais memoráveis. Além do sabor, prezamos pela experiência completa de compra, oferecendo atendimento personalizado, embalagens encantadoras e entrega rápida.', 'Alimentação', '@doceencanto', '(51) 99988-7766', 'contato@doceencanto.com', None, 1, -12.2642, -38.9546)

	adicionar_business('Aquarela Pet', 'A Aquarela Pet é uma loja completa para animais de estimação, oferecendo produtos de qualidade, acessórios exclusivos e atendimento personalizado. Aqui, cada cliente encontra soluções para cuidar, mimar e divertir seu pet. Também oferecemos serviços de banho, tosa e orientação nutricional, garantindo bem-estar e saúde aos animais. Nosso compromisso é com a felicidade e conforto de pets e seus tutores.', 'Pets e Animais', '@aquarelapet', '(71) 98712-3456', 'contato@aquarelapet.com', None, 7, -12.9704, -38.5123)

	adicionar_business('BookHouse', 'A BookHouse é uma livraria e espaço cultural que conecta leitores de todas as idades com livros, cursos e eventos. Aqui você encontra desde clássicos da literatura até lançamentos de autores independentes. Além da venda de livros, promovemos workshops, clubes de leitura e encontros literários, criando um ambiente rico em cultura e aprendizado.', 'Livros e Educação', '@bookhouse', '(71) 99887-6543', 'contato@bookhouse.com', None, 8, -12.9671, -38.5150)

	adicionar_business('Studio Verde', 'O Studio Verde é um espaço de jardinagem e paisagismo que transforma qualquer ambiente em um refúgio natural. Oferecemos consultoria, projetos personalizados e manutenção de jardins, buscando sempre integrar estética, sustentabilidade e praticidade. Nosso objetivo é proporcionar bem-estar e qualidade de vida por meio do contato com a natureza.', 'Serviços', '@studioverde', '(21) 91234-5670', 'contato@studioverde.com', None, 1, -12.9750, -38.5025)

	adicionar_business('Arte em Feltro', 'A Arte em Feltro é uma loja especializada em artesanato em feltro, oferecendo peças decorativas, brinquedos educativos e lembranças personalizadas. Cada item é feito à mão com cuidado e atenção aos detalhes, garantindo exclusividade e qualidade. Ideal para quem busca presentes criativos ou decoração charmosa.', 'Arte e Cultura', '@arteemfeltro', '(31) 98765-4320', 'contato@arteemfeltro.com', None, 1, -12.2700, -38.9500)

	for business_id in range(1, 11):
			for dia_semana in range(7):
				add_horario(business_id, dia_semana, "08:00", "18:00")
else:
	if __name__ == "__main__":
		init_db()

		registrar_user('Kaylon', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 12345-6789')

		tornar_admin(1)

		adicionar_business('Aurum Initium', 'Um curso voltado para construir uma base sólida em Matemática e Física, partindo do zero e avançando de forma estruturada. O foco é garantir compreensão profunda dos fundamentos, sem “atalhos”, para que o estudante tenha domínio real dos conceitos e esteja preparado para qualquer aprofundamento posterior — seja para vestibulares, olimpíadas ou estudos acadêmicos.', 'Livros e Educação', '@auruminitium', '(11) 91659-1346', 'kaylon.alt@outlook.com', None, 1, -12.1358, -40.36)

		for business_id in range(1, 11):
				for dia_semana in range(7):
					add_horario(business_id, dia_semana, "08:00", "18:00")
		app.run(host="0.0.0.0", debug=True)
