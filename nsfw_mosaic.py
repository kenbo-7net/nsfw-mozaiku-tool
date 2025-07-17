import os
import cv2
import torch
import requests
import numpy as np
from ultralytics import YOLO
from PIL import Image

# GitHub Releases からモデルを取得するURL（実際に自分でアップしたURLに置き換えてね）
MODEL_URL = 'https://github.com/kenbo-7net/nsfw-mozaiku-tool/releases/download/v1.0.0/genital.pt'
MODEL_PATH = 'genital.pt'

# ① genital.pt がなければダウンロード
if not os.path.exists(MODEL_PATH):
    print("🟡 genital.pt モデルをダウンロード中...")
    response = requests.get(MODEL_URL)
    if response.status_code == 200:
        with open(MODEL_PATH, 'wb') as f:
            f.write(response.content)
        print("✅ genital.pt を保存しました。")
    else:
        raise RuntimeError(f"❌ モデルのダウンロードに失敗しました: {response.status_code}")

# ② YOLO モデルを読み込み
model = YOLO(MODEL_PATH)

# ③ 処理関数：画像にモザイクをかける
def process_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            if image is None:
                print(f"⚠️ {filename} の読み込みに失敗しました。")
                continue

            results = model(image)[0]
            annotated_image = image.copy()

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # 検出された領域をモザイク処理
                roi = annotated_image[y1:y2, x1:x2]
                if roi.size == 0:
                    continue
                roi = cv2.resize(roi, (10, 10), interpolation=cv2.INTER_LINEAR)
                roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
                annotated_image[y1:y2, x1:x2] = roi

            # 保存
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, annotated_image)
            print(f"✅ {filename} を処理しました。")


            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, image)
