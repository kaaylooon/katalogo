from flask_socketio import SocketIO, join_room
from flask import session
from db.notifications import add_notification_db

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect():
	user_id = session.get("user_id")
	if user_id:
		join_room(f"user_{user_id}")
		print(f"Usuário {user_id} conectado ao SocketIO")

def send_notification(user_id, message):
	socketio.emit("new_notification", {"text": message}, room=f"user_{user_id}")
	add_notification_db(user_id, message)