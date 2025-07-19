import os
import zipfile
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images_and_log
from slack_sdk.webhook import WebhookClient

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ZIP_PATH = 'processed_images.zip'
CSV_PATH = 'detection_log.csv'
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")  # 環境変数から読み込む

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    for f in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, f))
    for f in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, f))
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)

    files = request.files.getlist('images')
    image_paths = []
    for file in files:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        image_paths.append(path)

    stats, processed_paths = process_images_and_log(image_paths, OUTPUT_FOLDER, CSV_PATH)

    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for path in processed_paths:
            zipf.write(path, arcname=os.path.basename(path))
        zipf.write(CSV_PATH, arcname='detection_log.csv')

    # Slack通知（任意）
    if SLACK_WEBHOOK_URL:
        webhook = WebhookClient(SLACK_WEBHOOK_URL)
        total = sum(stats.values())
        text = f"✅ モザイク処理完了\n合計画像数: {len(image_paths)}\n検出数: {total}\n詳細: {stats}"
        webhook.send(text=text)

    return jsonify({
        "message": "処理完了",
        "count": len(processed_paths),
        "zip_url": "/download"
    })

@app.route('/download')
def download():
    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

