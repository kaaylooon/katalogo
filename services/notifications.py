from db import add_notification_db
from services import send_notification

def add_notification(user_id, message):
	add_notification_db(user_id, message)
	send_notification(user_id, message)