from flask import Blueprint

from .feed import routes as feed_routes
from .business import routes as business_routes
from .user import routes as user_routes
from .admin import routes as admin_routes
from .checkout import routes as checkout_routes
from .comment import routes as comment_routes
from .home import routes as home_routes

def register_routes(app):
	app.register_blueprint(feed_routes)
	app.register_blueprint(business_routes)
	app.register_blueprint(user_routes)
	app.register_blueprint(admin_routes)
	app.register_blueprint(checkout_routes)
	app.register_blueprint(comment_routes)
	app.register_blueprint(home_routes)
