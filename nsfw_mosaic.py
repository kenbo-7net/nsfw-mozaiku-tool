import os
import cv2
import csv
import datetime
import requests
from ultralytics import YOLO

# モデルロード
model = YOLO('models/genital.pt')  # penis, vagina, anus の3クラス

# Slack連携（必要に応じて）
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')  # .envやRenderの環境変数に設定

def process_images(input_dir, output_dir, enable_csv=True, enable_slack=True):
    os.makedirs(output_dir, exist_ok=True)
    results_csv_path = os.path.join(output_dir, 'detection_results.csv')

    if enable_csv:
        csv_file = open(results_csv_path, mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Filename', 'Class', 'X1', 'Y1', 'X2', 'Y2'])

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path)

            # 検出
            results = model.predict(image)[0]
            boxes = results.boxes
            names = results.names if hasattr(results, 'names') else model.names

            for box in boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # CSV出力
                if enable_csv:
                    csv_writer.writerow([filename, label, x1, y1, x2, y2])

                # モザイク処理
                roi = image[y1:y2, x1:x2]
                if roi.size == 0: continue
                mosaic = cv2.resize(roi, (8, 8), interpolation=cv2.INTER_LINEAR)
                mosaic = cv2.resize(mosaic, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
                image[y1:y2, x1:x2] = mosaic

            cv2.imwrite(os.path.join(output_dir, filename), image)

    if enable_csv:
        csv_file.close()

    # Slack通知
    if enable_slack and SLACK_WEBHOOK_URL:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'✅ NSFWモザイク処理が完了しました。\n🕒 {timestamp}\n📦 出力先: `{output_dir}`'
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})
