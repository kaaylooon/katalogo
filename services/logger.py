import logging
from logging.handlers import RotatingFileHandler
import sys

# Cria o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # (DEBUG fica de fora)

# Formatter padrão
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Arquivo
file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=5*1024*1024,   # 5 MB por arquivo
    backupCount=3           # mantém 3 arquivos antigos
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.info("Logger iniciado com sucesso")
