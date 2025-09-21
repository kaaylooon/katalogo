from flask_limiter import Limiter
from flask import request
from flask_limiter.util import get_remote_address
from .logger import logger

def breach_callback(request_limit):
    ip = request.remote_addr
    endpoint = request.path
    logger.warning(f"Rate limit breached: {ip} - endpoint = {endpoint} - limite = {request_limit}")

# cria o Limiter sem app
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per day", "4 per hour"],
    on_breach=breach_callback
)

# Tá usando a memória, o que é arriscado (usuários podem burlar e fazer spam/flood). Mas foda-se por agora, certo? Tá dboa.
