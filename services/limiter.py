from flask_limiter import Limiter
from flask import request, session
from flask_limiter.util import get_remote_address
from .logger import logger


def limite_de_envios(request_limit):
	ip = request.remote_addr
	user = session.get("user_id", "anônimo")
	endpoint = request.path
	method = request.method
	user_agent = request.headers.get("User-Agent")
	query = request.query_string.decode()
	
	logger.warning(
		f"Rate limit breached: IP={ip}, Usuário={user}, Método={method}, "
		f"Endpoint={endpoint}, Limite={request_limit}, User-Agent={user_agent}, Query={query}"
	)

# cria o Limiter sem app
limiter = Limiter(
	key_func=get_remote_address,
	default_limits=[],
	on_breach=limite_de_envios
)

# Tá usando a memória, o que é arriscado (usuários podem burlar e fazer spam/flood). Mas foda-se por agora, certo? Tá dboa.
