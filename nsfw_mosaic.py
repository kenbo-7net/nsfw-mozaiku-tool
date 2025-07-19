import os
import cv2
import numpy as np
from ultralytics import YOLO

MODEL_PATH = "models/genital.pt"
TARGET_LABELS = {"penis", "vagina", "anus"}

model = YOLO(MODEL_PATH)

def apply_mosaic(image, x, y, w, h, mosaic_size=16):
    roi = image[y:y + h, x:x + w]
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y + h, x:x + w] = roi
    return image

def process_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for file in image_files:
        img_path = os.path.join(input_folder, file)
        image = cv2.imread(img_path)
        height, width = image.shape[:2]

        results = model(img_path, verbose=False)[0]

        for box in results.boxes:
            label = model.names[int(box.cls)]
            if label in TARGET_LABELS:
                conf = float(box.conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(width, x2)
                y2 = min(height, y2)
                w, h = x2 - x1, y2 - y1
                image = apply_mosaic(image, x1, y1, w, h)

        out_path = os.path.join(output_folder, file)
        cv2.imwrite(out_path, image)

