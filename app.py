
from flask import Flask, request, send_file
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def apply_blur(image_path, output_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    x1, y1 = int(w * 0.3), int(h * 0.3)
    x2, y2 = int(w * 0.7), int(h * 0.7)
    region = img[y1:y2, x1:x2]
    blurred = cv2.GaussianBlur(region, (51, 51), 0)
    img[y1:y2, x1:x2] = blurred
    cv2.imwrite(output_path, img)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")
        for file in files:
            filename = secure_filename(file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            file.save(input_path)
            apply_blur(input_path, output_path)
        zip_path = "blurred_images.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for fname in os.listdir(OUTPUT_FOLDER):
                zipf.write(os.path.join(OUTPUT_FOLDER, fname), fname)
        return send_file(zip_path, as_attachment=True)
    return '''
        <h1>NSFW画像ブラー処理</h1>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="images" multiple>
            <input type="submit" value="アップロードして処理">
        </form>
    '''

# ✅ Flaskアプリはここで起動（Render対応）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ← Renderは自動でPORTを割り当てる
    app.run(host="0.0.0.0", port=port)

