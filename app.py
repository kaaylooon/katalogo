from flask import Flask, jsonify, flash, redirect, url_for
from flask_limiter import RateLimitExceeded
from services.limiter import limiter
import arrow

from auth import auth
from db import init_db, seed_db

app = Flask(__name__)
limiter.init_app(app)

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    flash("Você atingiu o limite de envios. Tente novamente mais tarde. Em caso de uma tentativa de spam, saiba que a sua atividade será analisada pela equipe Katálogo.", "warning")

    return redirect(url_for("business.businesses"))

from routes.feed import routes as feed_routes
from routes.business import routes as business_routes
from routes.user import routes as user_routes
from routes.admin import routes as admin_routes
from routes.checkout import routes as checkout_routes
from routes.comment import routes as comment_routes
from routes.home import routes as home_routes

app.register_blueprint(feed_routes)
app.register_blueprint(business_routes)
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(checkout_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(home_routes)

app.register_blueprint(auth)

import os
from dotenv import load_dotenv
load_dotenv()
stripe_keys = {
	"STRIPE_API_KEY": os.environ.get('STRIPE_API_KEY'),
	"STRIPE_PUBLISHABLE_KEY": os.environ.get('STRIPE_PUBLISHABLE_KEY')
}

app.secret_key = os.environ.get('SECRET_KEY')

@app.route("/config")
def get_publishable_key():
	stripe_config = {"publicKey": stripe_keys["STRIPE_PUBLISHABLE_KEY"]}
	return jsonify(stripe_config)


def humanize_datetime(value):
	if not value:
		return ""
	return arrow.get(value, "YYYY-MM-DD HH:mm:ss").humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

DEPLOY = True

if DEPLOY:
	init_db()
	seed_db(full=True)
else:
	if __name__ == "__main__":
		init_db()
		seed_db(full=True)

		app.run(host="0.0.0.0", debug=True)