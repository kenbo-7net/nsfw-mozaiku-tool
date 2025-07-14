import os
import cv2
import numpy as np
from ultralytics import YOLO

def load_model():
    """YOLOモデルを読み込む"""
    model_path = os.path.join("yolo_models", "genital.pt")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"モデルファイルが見つかりません: {model_path}")
    return YOLO(model_path)

def detect_regions(model, image_path, conf_threshold=0.4):
    """画像内の検出領域を取得"""
    results = model(image_path, conf=conf_threshold)[0]
    detections = []
    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = r
        if conf > conf_threshold:
            detections.append((int(x1), int(y1), int(x2), int(y2)))
    return detections

def apply_mosaic(image_path, mosaic_size=30):
    """画像1枚に対してモザイクを適用"""
    try:
        model = load_model()
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"画像の読み込みに失敗しました: {image_path}")

        detections = detect_regions(model, image_path)

        for (x1, y1, x2, y2) in detections:
            roi = img[y1:y2, x1:x2]
            if roi.size == 0:
                continue
            roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(roi, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
            img[y1:y2, x1:x2] = roi

        return img
    except Exception as e:
        print(f"❌ モザイク処理失敗: {image_path}, エラー: {e}")
        return None

def process_images(image_paths, output_folder, mosaic_size=30, target="genitals"):
    """複数画像に一括でモザイク処理を実行"""
    os.makedirs(output_folder, exist_ok=True)
    processed_paths = []

    for image_path in image_paths:
        result = apply_mosaic(image_path, mosaic_size)
        if result is not None:
            filename = os.path.basename(image_path)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, result)
            processed_paths.append(output_path)

    print("✅ 一括モザイク処理完了")
    return processed_paths


