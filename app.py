from flask import Flask, request, send_file, render_template
from PIL import Image
import os
import zipfile
import shutil
import uuid
from nsfw_mosaic import apply_mosaic_batch

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ZIP_FOLDER = 'zips'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    mosaic_size = int(request.form.get('mosaic_size', 24))
    files = request.files.getlist('images')
    batch_id = str(uuid.uuid4())
    batch_folder = os.path.join(UPLOAD_FOLDER, batch_id)
    os.makedirs(batch_folder, exist_ok=True)

    images = []
    for file in files:
        file_path = os.path.join(batch_folder, file.filename)
        file.save(file_path)
        images.append(file_path)

    result_paths = apply_mosaic_batch(images, mosaic_size, RESULT_FOLDER)

    zip_path = os.path.join(ZIP_FOLDER, f"{batch_id}.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in result_paths:
            zipf.write(file_path, os.path.basename(file_path))

    shutil.rmtree(batch_folder)
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

