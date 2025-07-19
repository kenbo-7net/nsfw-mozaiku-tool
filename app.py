import os
import zipfile
import csv
import uuid
import shutil
import tempfile
import datetime
import json
import requests
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images_and_log

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
CSV_LOG = 'log.csv'
ZIP_FILE = 'processed_images.zip'
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # 環境変数で設定

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_folders():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
    if os.path.exists(CSV_LOG):
        os.remove(CSV_LOG)
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    clean_folders()
    files = request.files.getlist('images')

    image_paths = []
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        image_paths.append(path)

    stats, processed_paths = process_images_and_log(image_paths, OUTPUT_FOLDER, CSV_LOG)

    # ZIP化
    with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
        for fpath in processed_paths:
            zipf.write(fpath, arcname=os.path.basename(fpath))

    # Slack通知
    if SLACK_WEBHOOK_URL:
        summary = "\n".join([f"{cls}: {count}" for cls, count in stats.items()])
        msg = {
            "text": f"✅ モザイク処理完了 ({len(processed_paths)} 件)\n```{summary}```",
        }
        try:
            requests.post(SLACK_WEBHOOK_URL, json=msg)
        except Exception as e:
            print("Slack通知失敗:", e)

    return jsonify({
        "success": True,
        "count": len(processed_paths),
        "stats": stats
    })

@app.route('/download_zip')
def download_zip():
    return send_file(ZIP_FILE, as_attachment=True)

@app.route('/download_csv')
def download_csv():
    return send_file(CSV_LOG, as_attachment=True)

@app.route('/images')
def list_images():
    files = os.listdir(OUTPUT_FOLDER)
    return jsonify(sorted(files))

@app.route('/outputs/<filename>')
def get_image(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 10000)), host='0.0.0.0')
