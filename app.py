import os
import shutil
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from nsfw_mosaic import process_image
from batch_zipper import zip_processed_images

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
BATCH_SIZE = 100
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_images():
    if 'files' not in request.files:
        return "ファイルが見つかりません", 400

    files = request.files.getlist("files")
    mosaic_size = int(request.form.get("mosaic_size", 24))

    shutil.rmtree(PROCESSED_FOLDER, ignore_errors=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    batch_number = 0
    current_batch = []

    for i, file in enumerate(files):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        output_path = os.path.join(PROCESSED_FOLDER, filename)
        processed = process_image(input_path, output_path, mosaic_size)

        if processed:
            current_batch.append(output_path)

        if len(current_batch) >= BATCH_SIZE or i == len(files) - 1:
            zip_name = f"batch_{batch_number}.zip"
            zip_path = zip_processed_images(current_batch, zip_name)
            batch_number += 1
            current_batch = []

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)


