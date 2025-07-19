import os
import csv
import uuid
import zipfile
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images_and_log
from slack_sdk.webhook import WebhookClient

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
CSV_LOG = 'processing_log.csv'
ZIP_NAME = 'processed_images.zip'
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")  # .envで設定

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    uploaded_files = request.files.getlist('files[]')
    session_id = str(uuid.uuid4())[:8]
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    image_paths = []
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        image_paths.append(file_path)

    stats, processed_paths = process_images_and_log(
        image_paths=image_paths,
        output_dir=output_dir,
        csv_path=os.path.join(output_dir, CSV_LOG)
    )

    # zip化
    zip_path = os.path.join(output_dir, ZIP_NAME)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in processed_paths:
            arcname = os.path.basename(path)
            zipf.write(path, arcname)

    # Slack通知
    if SLACK_WEBHOOK_URL:
        msg = f"✅ モザイク処理完了\n📷 件数: {len(processed_paths)}枚\n📊 クラス統計: {stats}"
        webhook = WebhookClient(SLACK_WEBHOOK_URL)
        webhook.send(text=msg)

    # JSONで返す（表示用）
    return jsonify({
        'processed_images': [f"/{path}" for path in processed_paths],
        'zip_url': f"/{zip_path}",
        'csv_url': f"/{os.path.join(output_dir, CSV_LOG)}"
    })


@app.route('/<path:filename>')
def serve_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False, port=int(os.environ.get("PORT", 10000)), host='0.0.0.0')
