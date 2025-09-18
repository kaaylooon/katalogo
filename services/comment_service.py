from db import add_comentario
from services.logger import logger

def criar_comentario(user_id: int, business_id: int, content: str):
    add_comentario(user_id, business_id, content)
    logger.info(f"Novo comentário no negócio de ID {business_id}, pelo usuário de ID {user_id}")
