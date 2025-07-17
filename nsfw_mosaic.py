import os
import cv2
import numpy as np
import requests
from ultralytics import YOLO

# --- モデル設定 ---
MODEL_PATH = "models/genital.pt"
MODEL_URL = "https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0.0/genital.pt"
TARGET_LABELS = ['penis', 'vagina', 'anus']  # 陰部だけ

# --- モデルがなければ自動DL ---
if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt が見つかりません。ダウンロード中...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("✅ genital.pt を保存しました。")

# --- モデル読み込み ---
model = YOLO(MODEL_PATH)
print("✅ モデルロード完了")
print(f"📝 ラベル一覧: {model.names}")

# --- モザイク処理関数 ---
def apply_mosaic(image, x1, y1, x2, y2, mosaic_size=30):
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = roi
    return image

# --- メイン処理 ---
def process_images(input_folder='uploads', output_folder='outputs', mosaic_size=30):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        image = cv2.imread(input_path)
        if image is None:
            print(f"⚠️ 読み込めなかった画像: {filename}")
            continue

        results = model.predict(source=image, save=False, verbose=False)
        height, width = image.shape[:2]

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names.get(cls_id, 'unknown').lower()

                if label in TARGET_LABELS:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(width, x2), min(height, y2)
                    image = apply_mosaic(image, x1, y1, x2, y2, mosaic_size)

        cv2.imwrite(output_path, image)
        print(f"✅ モザイク完了: {filename}")

if __name__ == "__main__":
    process_images()
