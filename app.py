import os
import zipfile
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ZIP_PATH = 'processed_images.zip'
PORT = int(os.environ.get('PORT', 10000))  # Render用

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        os.makedirs(folder, exist_ok=True)
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    files = request.files.getlist('images')
    for file in files:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

    process_images(UPLOAD_FOLDER, OUTPUT_FOLDER)

    with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
        for root, _, files in os.walk(OUTPUT_FOLDER):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath, arcname=file)

    return send_file(ZIP_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=PORT)
