import os
import cv2
from ultralytics import YOLO

# モデルパス（genital.pt はプロジェクトルートに置く前提）
MODEL_PATH = 'genital.pt'

# YOLO モデルを初期化
model = YOLO(MODEL_PATH)

def mosaic_region(image, x1, y1, x2, y2, factor=15):
    region = image[y1:y2, x1:x2]
    small = cv2.resize(region, (max(1, (x2 - x1)//factor), max(1, (y2 - y1)//factor)))
    mosaic = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = mosaic
    return image

def process_images(input_dir='uploads', output_dir='output'):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            image = cv2.imread(input_path)
            if image is None:
                continue

            results = model.predict(source=input_path, conf=0.3)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

            for x1, y1, x2, y2 in boxes:
                h, w = image.shape[:2]
                x1 = max(0, min(x1, w - 1))
                x2 = max(0, min(x2, w - 1))
                y1 = max(0, min(y1, h - 1))
                y2 = max(0, min(y2, h - 1))
                image = mosaic_region(image, x1, y1, x2, y2)

            cv2.imwrite(output_path, image)

