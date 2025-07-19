import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/outputs'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# フォルダ初期化
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    files = os.listdir(OUTPUT_FOLDER)
    files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('index.html', files=files)

@app.route('/process', methods=['POST'])
def process():
    # 画像アップロード処理
    uploaded_files = request.files.getlist('images')
    for file in uploaded_files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

    # モザイク処理実行
    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER)

    return index()

# Render用PORT
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
