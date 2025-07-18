import os
import zipfile
from nsfw_mosaic import process_images

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ZIP_PATH = 'processed_images.zip'

# 初期化
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)
    for f in os.listdir(folder):
        os.remove(os.path.join(folder, f))

# モザイク処理
process_images(UPLOAD_FOLDER, OUTPUT_FOLDER, mosaic_size=30)

# ZIP作成
with zipfile.ZipFile(ZIP_PATH, 'w') as zipf:
    for filename in os.listdir(OUTPUT_FOLDER):
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        zipf.write(file_path, arcname=filename)

print(f"✅ Done! ZIP created: {ZIP_PATH}")
