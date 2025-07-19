import os
import cv2
import csv
from ultralytics import YOLO

model = YOLO("models/genital.pt")

def apply_mosaic(image, x1, y1, x2, y2, mosaic_rate=0.1):
    roi = image[y1:y2, x1:x2]
    small = cv2.resize(roi, (max(1, int((x2 - x1) * mosaic_rate)), max(1, int((y2 - y1) * mosaic_rate))))
    mosaic = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
    image[y1:y2, x1:x2] = mosaic
    return image

def process_images_and_log(image_paths, output_dir, csv_path):
    stats = {"penis": 0, "vagina": 0, "anus": 0}
    log_data = []
    processed_paths = []

    for img_path in image_paths:
        image = cv2.imread(img_path)
        results = model(img_path)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = results.names[cls_id]
            if label not in stats:
                continue

            stats[label] += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            h, w = image.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            image = apply_mosaic(image, x1, y1, x2, y2)

            log_data.append({
                "filename": os.path.basename(img_path),
                "class": label,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

        output_path = os.path.join(output_dir, os.path.basename(img_path))
        cv2.imwrite(output_path, image)
        processed_paths.append(output_path)

    # CSV出力
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["filename", "class", "x1", "y1", "x2", "y2"])
        writer.writeheader()
        writer.writerows(log_data)

        # 統計行（最後に追記）
        writer.writerow({})
        for cls, count in stats.items():
            writer.writerow({"filename": f"[STATS] {cls}", "class": count})

    return stats, processed_paths

