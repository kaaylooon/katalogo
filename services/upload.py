import os, uuid
from werkzeug.utils import secure_filename

# Pasta de uploads depende do ambiente
if os.environ.get("FLASK_ENV") == "development":
	UPLOAD_FOLDER = "/mock_data/uploads"  # pasta local para testes
else:
	UPLOAD_FOLDER = "/var/data/uploads"  # produção no Render

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Cria a pasta local se não existir
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder: str = UPLOAD_FOLDER) -> str:
	ext = file.filename.rsplit('.', 1)[1].lower()
	filename = f"{uuid.uuid4().hex}.{ext}"
	file.save(os.path.join(folder, secure_filename(filename)))
	return filename
