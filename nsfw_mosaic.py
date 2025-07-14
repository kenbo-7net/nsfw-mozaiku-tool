import os
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

# モデル選択関数
def get_model_path(target):
    if target == 'genitals+breast':
        return os.path.join("yolo_models", "genital_breast.pt")
    elif target == 'full':
        return os.path.join("yolo_models", "full_body.pt")
    else:
        return os.path.join("yolo_models", "genital.pt")

# モデル読み込み
def load_model(target):
    model_path = get_model_path(target)
    return YOLO(model_path)

# 検出
def detect_regions(model, image_path):
    results = model(image_path, conf=0.4)[0]
    detections = []
    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = r
        if conf > 0.4:
            detections.append((int(x1), int(y1), int(x2), int(y2)))
    return detections

# 単体画像処理
def apply_mosaic(image_path, mosaic_size=30, target='genitals'):
    model = load_model(target)
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

# 複数画像処理
def process_images(image_paths, output_folder, mosaic_size=30, target='genitals'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_paths = []
    for path in image_paths:
        img = apply_mosaic(path, mosaic_size, target)
        filename = os.path.basename(path)
        save_path = os.path.join(output_folder, filename)
        cv2.imwrite(save_path, img)
        output_paths.append(save_path)

    return output_paths


