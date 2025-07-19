import os
import zipfile
import csv
import shutil
import cv2
import datetime
import requests
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images_with_csv_and_stats

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
CSV_PATH = 'logs/results.csv'
ZIP_PATH = 'outputs/processed_images.zip'
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

def clear_folder(folder):
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        if os.path.isfile(path):
            os.remove(path)

def notify_slack(message):
    if SLACK_WEBHOOK:
        try:
            requests.post(SLACK_WEBHOOK, json={"text": message})
        except:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    clear_folder(OUTPUT_FOLDER)

    files = request.files.getlist("images")
    image_paths = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        image_paths.append(filepath)

    stats, processed_files = process_images_with_csv_and_stats(image_paths, OUTPUT_FOLDER, CSV_PATH)

    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for path in processed_files:
            zipf.write(path, arcname=os.path.basename(path))

    # Slack通知
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"✅ モザイク処理完了: {len(files)}件\n日付: {now}\nクラス内訳: {stats}"
    notify_slack(msg)

    return jsonify({"processed": [os.path.basename(p) for p in processed_files]})

@app.route('/outputs/<filename>')
def get_output_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename))

@app.route('/download')
def download():
    return send_file(ZIP_PATH, as_attachment=True)

@app.route('/clear', methods=['POST'])
def clear():
    clear_folder(UPLOAD_FOLDER)
    clear_folder(OUTPUT_FOLDER)
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False)
