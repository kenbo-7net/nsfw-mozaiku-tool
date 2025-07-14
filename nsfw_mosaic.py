import os
import cv2
import numpy as np
from ultralytics import YOLO

# モデルロード（genitals専用モデル）
model = YOLO("keremberke/yolov8n-porn")  # HuggingFaceのNSFWモデル

# ラベル名に応じた部位
TARGET_CLASSES = {
    'genitals': ['penis', 'vagina', 'anus'],
    'genitals+breast': ['penis', 'vagina', 'anus', 'female_breast'],
    'full': None  # 検出されたすべてにモザイク
}

def mosaic_area(img, x1, y1, x2, y2, size=24):
    area = img[y1:y2, x1:x2]
    area = cv2.resize(area, (size, size), interpolation=cv2.INTER_LINEAR)
    area = cv2.resize(area, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    img[y1:y2, x1:x2] = area
    return img

def process_images(image_paths, output_dir, mosaic_size, target='genitals'):
    target_classes = TARGET_CLASSES.get(target, ['penis', 'vagina', 'anus'])
    results = []

    for path in image_paths:
        img = cv2.imread(path)
        height, width = img.shape[:2]

        detections = model(img)[0]
        for box in detections.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            label = detections.names[cls]

            if target_classes is not None and label not in target_classes:
                continue
            if conf < 0.4:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)
            img = mosaic_area(img, x1, y1, x2, y2, size=mosaic_size)

        filename = os.path.basename(path)
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, img)
        results.append(save_path)

    return results

