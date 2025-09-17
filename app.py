from flask import Flask

import arrow

from routes import routes
from auth import auth

from db import init_db, seed_db

app = Flask(__name__)

app.secret_key = "secret_key"

app.register_blueprint(routes) 
app.register_blueprint(auth) 

def humanize_datetime(value):
		return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

DEPLOY = True

if __name__ == "__main__":
	init_db()
	seed_db(full=True)

	app.run(host="0.0.0.0", debug=not DEPLOY)