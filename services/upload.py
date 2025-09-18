import os, uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#verifica se o arquivo tem uma extensão válida.
def allowed_file(filename: str) -> bool:
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder: str = UPLOAD_FOLDER) -> str:
	ext = file.filename.rsplit('.', 1)[1].lower()
	filename = f"{uuid.uuid4().hex}.{ext}"
	file.save(os.path.join(folder, secure_filename(filename)))
	return filename