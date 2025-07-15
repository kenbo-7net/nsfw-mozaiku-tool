from flask import Flask, request, send_file, render_template
import os
import zipfile
import uuid
from nsfw_mosaic import process_images

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # UI用のHTMLを読み込む（任意）

@app.route('/process', methods=['POST'])
def process():
    files = request.files.getlist('images')
    session_id = str(uuid.uuid4())
    upload_path = os.path.join(UPLOAD_FOLDER, session_id)
    processed_path = os.path.join(PROCESSED_FOLDER, session_id)
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(processed_path, exist_ok=True)

    image_paths = []
    for file in files:
        path = os.path.join(upload_path, file.filename)
        file.save(path)
        image_paths.append(path)

    process_images(image_paths, processed_path)

    zip_path = f"{processed_path}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in os.listdir(processed_path):
            zipf.write(os.path.join(processed_path, file), arcname=file)

    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

