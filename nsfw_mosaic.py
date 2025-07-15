import os
import cv2
import numpy as np
from ultralytics import YOLO

# -------------------------
# 設定
# -------------------------
MODEL_DIR = "yolo_models"
MODEL_PATH = os.path.join(MODEL_DIR, "genital.pt")
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/model/genital.pt"  # ここにあなたの正しいURLを設定

MOS_SIZE = 40  # モザイクのピクセルサイズ

# -------------------------
# モデルが存在しなければダウンロード
# -------------------------
if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt モデルをダウンロード中...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    import requests
    r = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    print("✅ genital.pt を保存しました。")

# -------------------------
# モデルの読み込み（weights_only=False 相当）
# -------------------------
model = YOLO(MODEL_PATH, task='detect')


# -------------------------
# モザイク処理関数
# -------------------------
def mosaic_area(img, x1, y1, x2, y2, size=MOS_SIZE):
    roi = img[y1:y2, x1:x2]
    roi = cv2.resize(roi, ((x2 - x1) // size, (y2 - y1) // size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    img[y1:y2, x1:x2] = roi
    return img


# -------------------------
# 画像群を処理する関数
# -------------------------
def process_images(image_paths, conf=0.4):
    results = []

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"⚠️ 読み込み失敗: {path}")
            continue

        height, width, _ = img.shape
        detections = model(path, conf=conf)[0].boxes

        for box in detections:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1 = max(x1, 0)
            y1 = max(y1, 0)
            x2 = min(x2, width)
            y2 = min(y2, height)

            img = mosaic_area(img, x1, y1, x2, y2)

        results.append((path, img))

    return results

    return output_image
