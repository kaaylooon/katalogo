import psycopg2
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "db.db")

def get_connection():
	DATABASE_URL = os.getenv("DATABASE_URL")
	conn = psycopg2.connect(DATABASE_URL)
	return conn
