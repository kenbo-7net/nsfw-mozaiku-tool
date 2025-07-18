import os
import cv2
from ultralytics import YOLO
from utils import load_image, apply_mosaic
import urllib.request

# モデルのパスとダウンロードURL
MODEL_PATH = "models/genital.pt"
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0.1/genital.pt"

# モザイクサイズ（pixel単位で自動調整）
DEFAULT_MOSAIC_SIZE = 30

# 対象クラス名（正確に3つ）
TARGET_LABELS = ["penis", "vagina", "anus"]

def download_model_if_needed():
    if not os.path.exists(MODEL_PATH):
        print("💾 genital.pt not found. Downloading...")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("✅ Download complete.")

def process_images(input_folder, output_folder, mosaic_size=DEFAULT_MOSAIC_SIZE):
    download_model_if_needed()

    print("📦 Loading model...")
    model = YOLO(MODEL_PATH)
    print(f"🧠 Classes in model: {model.names}")

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue

        image_path = os.path.join(input_folder, filename)
        image = load_image(image_path)
        print(f"🔍 Processing: {filename}")

        results = model.predict(source=image, conf=0.3, iou=0.3, verbose=False)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label not in TARGET_LABELS:
                continue  # 他の部位（胸など）は無視

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            image = apply_mosaic(image, x1, y1, x2, y2, mosaic_size)

        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)
        print(f"✅ Saved: {output_path}")


if __name__ == "__main__":
    process_images()
