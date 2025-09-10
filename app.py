from flask import Flask
from werkzeug.security import generate_password_hash

import arrow

from routes import routes
from auth import auth

from db import init_db, tornar_admin, registrar_user, adicionar_business, add_feed

app = Flask(__name__)

app.secret_key = "aEfGbhD"

app.register_blueprint(routes) 
app.register_blueprint(auth) 

def humanize_datetime(value):
		return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

init_db()
registrar_user('Kaylon', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 12345-6789')
tornar_admin(1)

#if __name__ == "__main__":
#	init_db()
#
#	registrar_user('Kaylon Souza', 'kaylon.contact@gmail.com', generate_password_hash('adm123'), '(11) 91659-1346')
#	tornar_admin(1)

#	app.run(debug=True, host='0.0.0.0')
