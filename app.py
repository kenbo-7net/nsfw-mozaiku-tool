import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ZIP_PATH = 'processed_images.zip'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def init_folders():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    init_folders()
    mosaic_size = int(request.form.get('mosaic_size', 30))

    files = request.files.getlist('images')
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER, mosaic_size)

    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for filename in os.listdir(OUTPUT_FOLDER):
            filepath = os.path.join(OUTPUT_FOLDER, filename)
            zipf.write(filepath, arcname=filename)

    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # ← Renderはここからポート番号を受け取る
    app.run(host="0.0.0.0", port=port, debug=False)  # ← 必ず 0.0.0.0 にする
