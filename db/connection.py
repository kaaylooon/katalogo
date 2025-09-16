import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "db.db")

def get_connection():
    return sqlite3.connect(DB_NAME)
