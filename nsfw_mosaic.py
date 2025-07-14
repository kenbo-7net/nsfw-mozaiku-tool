import cv2
import numpy as np
import os

# モザイクの強さ調整
DEFAULT_MOSAIC_SIZE = 24

# 今は仮の矩形を使ったランダム検出（学習モデルと差し替え可能）
def detect_sensitive_areas(image):
    height, width = image.shape[:2]
    # デモ用に中央部分に矩形を仮配置
    return [
        (int(width * 0.45), int(height * 0.6), int(width * 0.1), int(height * 0.15))  # x, y, w, h
    ]

def apply_mosaic(image, areas, mosaic_size=DEFAULT_MOSAIC_SIZE):
    for (x, y, w, h) in areas:
        roi = image[y:y+h, x:x+w]
        roi = cv2.resize(roi, (mosaic_size, mosaic_size), interpolation=cv2.INTER_LINEAR)
        roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
        image[y:y+h, x:x+w] = roi
    return image

def process_image(input_path, output_path, mosaic_size=DEFAULT_MOSAIC_SIZE):
    image = cv2.imread(input_path)
    if image is None:
        print(f"画像読み込み失敗: {input_path}")
        return False

    areas = detect_sensitive_areas(image)
    if not areas:
        print("検出部位なし → 処理スキップ")
        return False

    result = apply_mosaic(image, areas, mosaic_size)
    cv2.imwrite(output_path, result)
    return True
