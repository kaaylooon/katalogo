import os, uuid
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/var/data/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder: str = UPLOAD_FOLDER) -> str:
	ext = file.filename.rsplit('.', 1)[1].lower()
	filename = f"{uuid.uuid4().hex}.{ext}"
	file.save(os.path.join(folder, secure_filename(filename)))
	return filename
