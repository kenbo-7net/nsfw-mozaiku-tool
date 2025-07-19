import os
import cv2
import csv
import time
import datetime
import requests
from collections import defaultdict
from ultralytics import YOLO

model = YOLO('models/genital.pt')  # penis, vagina, anus

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

def process_images(input_dir, output_dir, enable_csv=True, enable_slack=True):
    os.makedirs(output_dir, exist_ok=True)
    results_csv_path = os.path.join(output_dir, 'detection_results.csv')

    total_detections = 0
    class_counter = defaultdict(int)
    image_counter = 0

    if enable_csv:
        csv_file = open(results_csv_path, mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Filename', 'Class', 'X1', 'Y1', 'X2', 'Y2'])

    start_time = time.time()

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)
        results = model.predict(image)[0]
        boxes = results.boxes
        names = results.names if hasattr(results, 'names') else model.names

        image_detections = 0

        for box in boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # ログ記録
            if enable_csv:
                csv_writer.writerow([filename, label, x1, y1, x2, y2])

            class_counter[label] += 1
            total_detections += 1
            image_detections += 1

            # モザイク処理
            roi = image[y1:y2, x1:x2]
            if roi.size == 0: continue
            mosaic = cv2.resize(roi, (8, 8), interpolation=cv2.INTER_LINEAR)
            mosaic = cv2.resize(mosaic, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
            image[y1:y2, x1:x2] = mosaic

        if image_detections > 0:
            cv2.imwrite(os.path.join(output_dir, filename), image)

        image_counter += 1

    # CSVに合計件数追記
    if enable_csv:
        csv_writer.writerow([])
        csv_writer.writerow(['--- Summary ---'])
        csv_writer.writerow(['Total Images Processed', image_counter])
        csv_writer.writerow(['Total Detections', total_detections])
        for cls, count in class_counter.items():
            csv_writer.writerow([f'Class: {cls}', f'{count} items'])
        csv_file.close()

    # Slack通知（オプション）
    if enable_slack and SLACK_WEBHOOK_URL:
        elapsed = round(time.time() - start_time, 2)
        summary = "\n".join([f"・{cls}: {count}件" for cls, count in class_counter.items()])
        message = (
            f"✅ *NSFWモザイク処理が完了しました*\n"
            f"🖼️ 処理画像数: *{image_counter}枚*\n"
            f"🔍 検出総数: *{total_detections}件*\n"
            f"{summary}\n"
            f"🕒 所要時間: {elapsed}秒\n"
            f"📁 出力先: `{output_dir}`"
        )
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})
