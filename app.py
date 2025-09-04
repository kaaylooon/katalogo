from flask import Flask

from routes import routes
from auth import auth

from db import init_db

app = Flask(__name__)

app.secret_key = "aEfGbhD"

app.register_blueprint(routes) 
app.register_blueprint(auth) 

if __name__ == "__main__":
	init_db()
	app.run(debug=True)
