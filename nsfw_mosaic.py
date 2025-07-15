import os
import cv2
import numpy as np
import requests
from ultralytics import YOLO

# モデル設定
MODEL_PATH = "genital.pt"
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0.0/genital.pt"

# モデルがなければ自動ダウンロード
if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt モデルをダウンロード中...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
    print("✅ genital.pt を保存しました。")

# YOLO モデル読み込み
model = YOLO(MODEL_PATH)

def apply_mosaic(image, x, y, w, h, mosaic_size=10):
    roi = image[y:y+h, x:x+w]
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y+h, x:x+w] = roi
    return image

def process_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            results = model(image)
            result = results[0]
            boxes = result.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = box.astype(int)
                x = max(x1, 0)
                y = max(y1, 0)
                w = max(x2 - x1, 1)
                h = max(y2 - y1, 1)
                image = apply_mosaic(image, x, y, w, h)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
