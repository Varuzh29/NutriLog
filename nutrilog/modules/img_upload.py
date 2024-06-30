from flask import url_for, current_app as app
from werkzeug.utils import secure_filename
import os
from PIL import Image
import uuid


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['IMG_ALLOWED_EXTENSIONS']


def upload_img(file):
    error = None
    if file and allowed_file(file.filename):
        with Image.open(file) as image:
            image = image.convert('RGB')
            image = image.resize(app.config['IMG_SIZE'])
            filename = secure_filename(str(uuid.uuid4()) + '.webp')
            filepath = os.path.join(app.instance_path, app.config['IMG_UPLOAD_PATH'], filename)
            image.save(filepath, optimize=True, quality=70, format='WEBP')
            return url_for('diary.uploaded_file', filename=filename), None
    else:
        error = 'File type not allowed'
    return None, error
