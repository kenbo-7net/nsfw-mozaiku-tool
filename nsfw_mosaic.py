import os
import cv2
import numpy as np
from ultralytics import YOLO

# モデルを読み込み（1回のみ）
model_path = os.path.join("yolo_models", "genital.pt")
model = YOLO(model_path)

def detect_genitals(image_path, conf_threshold=0.4):
    results = model(image_path, conf=conf_threshold)[0]
    detections = []
    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = r
        if conf > conf_threshold:
            detections.append((int(x1), int(y1), int(x2), int(y2)))
    return detections

def mosaic_region(img, x1, y1, x2, y2, mosaic_size):
    roi = img[y1:y2, x1:x2]
    if roi.size == 0:
        return
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    img[y1:y2, x1:x2] = roi

def apply_mosaic_to_image(image_path, output_path, mosaic_size=30):
    img = cv2.imread(image_path)
    detections = detect_genitals(image_path)

    for (x1, y1, x2, y2) in detections:
        mosaic_region(img, x1, y1, x2, y2, mosaic_size)

    cv2.imwrite(output_path, img)

def process_images(image_paths, output_dir, mosaic_size=30, target="genitals"):
    output_paths = []

    os.makedirs(output_dir, exist_ok=True)

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        apply_mosaic_to_image(image_path, output_path, mosaic_size)
        output_paths.append(output_path)

    return output_paths
