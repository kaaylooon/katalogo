from flask import Flask
import arrow

import os
from dotenv import load_dotenv

from auth import auth
from db import init_db, seed_db

from routes.feed import routes as feed_routes
from routes.business import routes as business_routes
from routes.user import routes as user_routes
from routes.admin import routes as admin_routes
from routes.checkout import routes as checkout_routes
from routes.comment import routes as comment_routes
from routes.home import routes as home_routes


load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

app.register_blueprint(feed_routes)
app.register_blueprint(business_routes)
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(checkout_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(home_routes)
app.register_blueprint(auth) 


def humanize_datetime(value):
	if not value:
		return ""
	return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime


DEPLOY = False

if DEPLOY:
	init_db()
	seed_db(full=True)
else:
	if __name__ == "__main__":
		init_db()
		seed_db(full=True)

		app.run(host="0.0.0.0", debug=True)