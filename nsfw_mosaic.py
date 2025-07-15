import cv2
import os
from ultralytics import YOLO

MODEL_PATH = 'genital.pt'  # ダウンロード済みモデルファイル名
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# YOLOv8でgenital.ptを読み込む（task='detect'は明示しなくてもOK）
model = YOLO(MODEL_PATH)

def apply_mosaic(image, x, y, w, h, mosaic_size=10):
    roi = image[y:y + h, x:x + w]
    roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
    roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y + h, x:x + w] = roi
    return image

def process_images(input_dir='uploads', output_dir=OUTPUT_DIR):
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue

        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"画像の読み込みに失敗しました: {filename}")
            continue

        results = model.predict(source=image_path, conf=0.3, iou=0.5)
        detections = results[0].boxes.xyxy.cpu().numpy().astype(int)

        for (x1, y1, x2, y2) in detections:
            image = apply_mosaic(image, x1, y1, x2 - x1, y2 - y1)

        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, image)
        print(f"[✅] {filename} を処理して保存しました")

if __name__ == '__main__':
    process_images()

