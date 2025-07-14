import os
import zipfile
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_images

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ZIP_NAME = 'mosaic_result.zip'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    images = request.files.getlist('images')
    mosaic_size = int(request.form.get('mosaic_size', 24))
    target = request.form.get('target', 'genitals')  # 'genitals', 'genitals+breast', 'full'

    image_paths = []
    for img in images[:100]:  # 最大100枚
        filename = secure_filename(img.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(save_path)
        image_paths.append(save_path)

    output_paths = process_images(image_paths, RESULT_FOLDER, mosaic_size, target)

    zip_path = os.path.join(RESULT_FOLDER, ZIP_NAME)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in output_paths:
            arcname = os.path.basename(path)
            zipf.write(path, arcname)

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

