import os
import zipfile
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ZIP_PATH = 'processed_images.zip'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # フォルダを初期化
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    # パラメータ取得
    mosaic_size = int(request.form.get('mosaic_size', 30))

    # 画像保存
    files = request.files.getlist('images')
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    # モザイク処理（オプション付き）
    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER, mosaic_size=mosaic_size)

    # ZIP圧縮
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for fname in os.listdir(OUTPUT_FOLDER):
            zipf.write(os.path.join(OUTPUT_FOLDER, fname), arcname=fname)

    return redirect('/download')

@app.route('/download')
def download():
    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
