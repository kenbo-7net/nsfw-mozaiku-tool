import os
import cv2
import torch
import requests
from ultralytics import YOLO
from utils import apply_mosaic

MODEL_DIR = "yolo_models"
MODEL_PATH = os.path.join(MODEL_DIR, "genital.pt")
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/model/genital.pt"

# モデルの自動ダウンロード
def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        print("🟡 genital.pt モデルをダウンロード中...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ genital.pt を保存しました。")

download_model()

# YOLO モデル読み込み
model = YOLO(MODEL_PATH)

# 検出カテゴリごとのラベル
CLASS_MAP = {
    0: 'penis',
    1: 'vagina',
    2: 'anus'
}

def detect_and_mosaic(image_path, mosaic_size=25, detection_mode="genitals"):
    image = cv2.imread(image_path)
    results = model(image)[0]

    h, w, _ = image.shape
    regions = []

    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        label = CLASS_MAP.get(cls_id, None)
        if label is None:
            continue

        # 検出対象かどうか確認
        if detection_mode == "genitals" and label not in ['penis', 'vagina', 'anus']:
            continue
        elif detection_mode == "genitals+breast" and label not in ['penis', 'vagina', 'anus', 'breast']:
            continue
        elif detection_mode == "full":
            pass  # 全て適用

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        regions.append((x1, y1, x2, y2))

    # モザイク適用
    output_image = apply_mosaic(image, regions, mosaic_size)
    return output_image

