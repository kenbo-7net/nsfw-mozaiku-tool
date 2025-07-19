import os
import cv2
from ultralytics import YOLO

# モデルの読み込み
model = YOLO('models/genital.pt')
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# モザイク処理関数
def mosaic_area(image, x, y, w, h, ratio=0.1):
    mosaic = image[y:y+h, x:x+w]
    small = cv2.resize(mosaic, (max(1, int(w*ratio)), max(1, int(h*ratio))), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y+h, x:x+w] = mosaic
    return image

# 画像を一括で処理
def process_images(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        name, ext = os.path.splitext(filename.lower())
        if ext not in ALLOWED_EXTENSIONS:
            continue

        path = os.path.join(input_folder, filename)
        image = cv2.imread(path)
        if image is None:
            continue

        # 推論
        results = model(path)[0]
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls not in [0, 1, 2]:  # penis, vagina, anus のみ
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(image.shape[1], x2), min(image.shape[0], y2)
            image = mosaic_area(image, x1, y1, x2 - x1, y2 - y1)

        # 保存
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)


