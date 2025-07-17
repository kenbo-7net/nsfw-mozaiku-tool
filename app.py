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

# ルートページ
@app.route('/')
def index():
    return render_template('index.html')

# POST処理
@app.route('/upload', methods=['POST'])
def upload():
    # アップロードフォルダ初期化
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                os.remove(os.path.join(folder, f))
        else:
            os.makedirs(folder)

    # ファイル保存
    files = request.files.getlist('images')
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # モザイク処理
    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER)

    # ZIP圧縮
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for fname in os.listdir(OUTPUT_FOLDER):
            fpath = os.path.join(OUTPUT_FOLDER, fname)
            zipf.write(fpath, arcname=fname)

    return redirect('/download')

# ダウンロード用ルート
@app.route('/download')
def download():
    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
