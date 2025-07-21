import os
import xml.etree.ElementTree as ET

# 入力と出力のディレクトリパス
input_dir = "./labelImg/annotations"
output_dir = "./labelImg/labels"
os.makedirs(output_dir, exist_ok=True)

# クラス名のマッピング（必要なら追加）
class_mapping = {
    "penis": 0,
    "vagina": 1,
    "anus": 2
}

# デバッグ出力
print(f"📂 入力XML数: {len(os.listdir(input_dir))}")

for file in os.listdir(input_dir):
    if not file.endswith(".xml"):
        continue

    input_path = os.path.join(input_dir, file)
    tree = ET.parse(input_path)
    root = tree.getroot()

    # サイズ取得
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    # 出力先のtxtファイルパス
    output_path = os.path.join(output_dir, file.replace(".xml", ".txt"))

    with open(output_path, "w") as f:
        for obj in root.findall("object"):
            label = obj.find("name").text

            if label not in class_mapping:
                print(f"⚠ 未知ラベル: {label} in {file}")
                continue

            class_id = class_mapping[label]
            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            # YOLO形式 (x_center, y_center, width, height)
            x_center = ((xmin + xmax) / 2) / w
            y_center = ((ymin + ymax) / 2) / h
            box_w = (xmax - xmin) / w
            box_h = (ymax - ymin) / h

            line = f"{class_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}\n"
            f.write(line)
        
    print(f"✅ 変換完了: {file} → {output_path}")

