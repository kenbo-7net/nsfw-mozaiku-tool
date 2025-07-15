import os
import cv2
import numpy as np
import requests
from ultralytics import YOLO

MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0/genital.pt"
MODEL_PATH = "genital.pt"

# モデルがなければGitHubからDL
if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt モデルをダウンロード中...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("✅ genital.pt を保存しました。")

model = YOLO(MODEL_PATH)

def apply_mosaic(img, x1, y1, x2, y2, mosaic_scale=0.05):
    roi = img[y1:y2, x1:x2]
    roi_small = cv2.resize(roi, (max(1, int((x2 - x1) * mosaic_scale)), max(1, int((y2 - y1) * mosaic_scale))))
    roi_mosaic = cv2.resize(roi_small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    img[y1:y2, x1:x2] = roi_mosaic
    return img

def process_images(image_paths, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for path in image_paths:
        img = cv2.imread(path)
        results = model(img)[0]
        for box in results.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            img = apply_mosaic(img, x1, y1, x2, y2)
        filename = os.path.basename(path)
        cv2.imwrite(os.path.join(output_dir, filename), img)

