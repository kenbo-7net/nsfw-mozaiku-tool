import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images  # 自作モジュール（存在前提）

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
    # アップロードフォルダ初期化
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    # アップロードファイルを保存
    uploaded_files = request.files.getlist('images')
    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    # モザイク処理
    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER)

    # ZIPファイル作成
    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for filename in os.listdir(OUTPUT_FOLDER):
            zipf.write(os.path.join(OUTPUT_FOLDER, filename), filename)

    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    # Renderで自動取得されるポート番号を取得して使う
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

