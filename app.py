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

# トップページ
@app.route('/')
def index():
    return render_template('index.html')

# モザイク処理とZIP返却
@app.route('/process', methods=['POST'])
def process():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))

    files = request.files.getlist('images')
    filepaths = []

    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        filepaths.append(path)

    # モザイク処理
    process_images(filepaths, OUTPUT_FOLDER)

    # ZIP化
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for fname in os.listdir(OUTPUT_FOLDER):
            fpath = os.path.join(OUTPUT_FOLDER, fname)
            zipf.write(fpath, arcname=fname)

    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
