import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from utils import apply_mosaic
from datetime import datetime

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return 'ファイルが見つかりません'

    files = request.files.getlist('images')
    result_urls = []

    for file in files[:400]:  # 最大400枚まで制限
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            output_filename = f"{timestamp}_{filename}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            file.save(input_path)

            # モザイク処理
            image = cv2.imread(input_path)
            h, w = image.shape[:2]

            # 陰部（中央付近を仮定）をざっくり検出し範囲指定
            center_x, center_y = w // 2, h // 2
            bbox_w, bbox_h = w // 5, h // 5
            bboxes = [(center_x - bbox_w // 2, center_y - bbox_h // 2, bbox_w, bbox_h)]

            result = apply_mosaic(image, bboxes, ratio=0.02)  # ← 濃いめのモザイク
            cv2.imwrite(input_path, result)

            result_urls.append(f'/static/{output_filename}')

    return render_template('index.html', result_urls=result_urls)

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

