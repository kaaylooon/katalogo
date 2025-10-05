from flask import Flask, jsonify, flash, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import RateLimitExceeded
from services import *

import arrow
import os
from dotenv import load_dotenv

from auth import auth
from db import init_db, seed_db, get_user_notifications

app = Flask(__name__)
limiter.init_app(app)
load_dotenv()

stripe_keys = {
	"STRIPE_API_KEY": os.environ.get('STRIPE_API_KEY'),
	"STRIPE_PUBLISHABLE_KEY": os.environ.get('STRIPE_PUBLISHABLE_KEY')
}

app.secret_key = os.environ.get('SECRET_KEY')

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = '/var/data/uploads'

socketio.init_app(app)

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
	flash("Você atingiu o limite de envios. Tente novamente mais tarde. Em caso de uma tentativa de spam, saiba que a sua atividade será analisada pela equipe Katálogo.", "warning")
	logger.warning(str(e))
	return redirect(url_for("business.businesses"))


from routes.feed import routes as feed_routes
from routes.business import routes as business_routes
from routes.user import routes as user_routes
from routes.admin import routes as admin_routes
from routes.checkout import routes as checkout_routes
from routes.comment import routes as comment_routes
from routes.home import routes as home_routes
from routes.service import routes as service_routes

app.register_blueprint(feed_routes)
app.register_blueprint(business_routes)
app.register_blueprint(user_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(checkout_routes)
app.register_blueprint(comment_routes)
app.register_blueprint(home_routes)
app.register_blueprint(service_routes)

app.register_blueprint(auth)

db = SQLAlchemy(app)

if os.environ.get("FLASK_ENV") == "development":
	UPLOAD_FOLDER = "./mock_data/uploads"  # pasta local para testes
else:
	UPLOAD_FOLDER = "/var/data/uploads"  # produção no Render

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/config")
def get_publishable_key():
	stripe_config = {"publicKey": stripe_keys["STRIPE_PUBLISHABLE_KEY"]}
	return jsonify(stripe_config)

def humanize_datetime(value):
	if not value:
		return ""
	return arrow.get(value).humanize(locale="pt_br")
app.jinja_env.filters['humandate'] = humanize_datetime

DEPLOY = False

if DEPLOY:
	init_db()
	seed_db(full=False)
else:
	if __name__ == "__main__":
		init_db()
		seed_db(full=False)

		socketio.run(app, host="0.0.0.0", debug=True)