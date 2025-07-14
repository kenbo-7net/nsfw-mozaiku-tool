from flask import Flask, render_template, request, send_from_directory
import os
from utils import process_images
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('images')
        task_id = str(uuid.uuid4())
        task_dir = os.path.join(app.config['RESULT_FOLDER'], task_id)
        os.makedirs(task_dir, exist_ok=True)

        image_paths = []
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_paths.append(filepath)

        result_files = process_images(image_paths, task_dir)
        return render_template('index.html', result_files=result_files, task_id=task_id)

    return render_template('index.html')

@app.route('/download/<task_id>/<filename>')
def download(task_id, filename):
    return send_from_directory(os.path.join(RESULT_FOLDER, task_id), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
