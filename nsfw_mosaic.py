import os
import cv2
import torch
import requests
from ultralytics.models.yolo.detect import DetectionModel
from utils import apply_mosaic

MODEL_DIR = "yolo_models"
MODEL_PATH = os.path.join(MODEL_DIR, "genital.pt")
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/model/genital.pt"

# モデルをダウンロード
def download_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        print("🟡 genital.pt モデルをダウンロード中...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ genital.pt を保存しました。")

download_model()

# 安全にモデル読み込み（weights_only=False 指定）
def load_model(path):
    print("📦 YOLO モデルを読み込み中...")
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    model = DetectionModel(cfg=ckpt['model'].yaml)
    model.load_state_dict(ckpt['model'].float().state_dict())
    model.eval()
    return model

model = load_model(MODEL_PATH)

# ラベルマッピング
CLASS_MAP = {
    0: 'penis',
    1: 'vagina',
    2: 'anus'
}

def detect_and_mosaic(image_path, mosaic_size=25, detection_mode="genitals"):
    image = cv2.imread(image_path)
    results = model.predict(image)[0]  # ultralyticsモデルと同様に扱えるように構成

    h, w, _ = image.shape
    regions = []

    for box in results.boxes:
        cls_id = int(box.cls[0].item())
        label = CLASS_MAP.get(cls_id)
        if label is None:
            continue

        if detection_mode == "genitals" and label not in ['penis', 'vagina', 'anus']:
            continue
        elif detection_mode == "genitals+breast" and label not in ['penis', 'vagina', 'anus', 'breast']:
            continue

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        regions.append((x1, y1, x2, y2))

    output_image = apply_mosaic(image, regions, mosaic_size)
    return output_image
