import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
file_handler.setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)