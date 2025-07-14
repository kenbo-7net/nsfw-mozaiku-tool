import os
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

def load_model():
    model_path = os.path.join("yolo_models", "genital.pt")  # 学習済みモデル
    return YOLO(model_path)

def detect_regions(model, image_path):
    results = model(image_path, conf=0.4)[0]
    detections = []
    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = r
        if conf > 0.4:
            detections.append((int(x1), int(y1), int(x2), int(y2)))
    return detections

def apply_mosaic(image_path, mosaic_size=30):
    model = load_model()
    img = cv2.imread(image_path)
    detections = detect_regions(model, image_path)

    for (x1, y1, x2, y2) in detections:
        roi = img[y1:y2, x1:x2]
        if roi.size == 0:
            continue
        roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
        roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        img[y1:y2, x1:x2] = roi

    return img

def batch_process(input_folder, output_folder, mosaic_size=30):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg')):
            image_path = os.path.join(input_folder, filename)
            out_image = apply_mosaic(image_path, mosaic_size)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, out_image)

    print("✅ 全バッチ処理完了")


