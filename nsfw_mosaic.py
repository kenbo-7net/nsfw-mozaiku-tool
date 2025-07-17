import os
import cv2
import numpy as np
from ultralytics import YOLO
import requests

# genital.pt を自動ダウンロード
MODEL_PATH = 'genital.pt'
MODEL_URL = 'https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0.0/genital.pt'

if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt モデルをダウンロード中...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)
    print("✅ genital.pt を保存しました。")

# モデル読み込み
model = YOLO(MODEL_PATH)

# 検出したラベルにモザイク処理をかける関数
def apply_mosaic(image, x1, y1, x2, y2, mosaic_size=30):
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        return image
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = roi
    return image

# メイン関数（Flask から呼び出される）
def process_images(input_folder, output_folder, mosaic_size=30):
    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        input_path = os.path.join(input_folder, filename)
        image = cv2.imread(input_path)
        if image is None:
            continue

        height, width = image.shape[:2]

        # YOLO 推論
        results = model.predict(source=image, save=False, verbose=False)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]

                # モザイク対象ラベルのみ処理
                if label.lower() in ['penis', 'vagina', 'anus']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(width, x2), min(height, y2)
                    image = apply_mosaic(image, x1, y1, x2, y2, mosaic_size=mosaic_size)

        # 出力保存
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
