import logging
import sys

# Cria o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # (DEBUG fica de fora)

# Formatter padrão
formatter = logging.Formatter(
	"%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	"%Y-%m-%dT%H:%M:%S"
)

# Apenas console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def log_event(title: str, level=logging.WARNING, **kwargs):
	parts = [f"## {title}"] + [f"{k}: {v}" for k, v in kwargs.items()]
	logger.log(level, " | ".join(parts))

if __name__ == "__main__":
	logger.info("Logger iniciado com sucesso")
