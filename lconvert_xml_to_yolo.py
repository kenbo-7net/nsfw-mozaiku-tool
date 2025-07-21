import os
import xml.etree.ElementTree as ET

# カテゴリ一覧（順番大事！）
classes = ["penis", "vagina", "anus"]

# XMLファイルのフォルダ
input_dir = r"C:\Users\next stage marketing\OneDrive\ドキュメント\GitHub\nsfw-mozaiku-tool\labelImg\annotations"
output_dir = input_dir  # 同じ場所に.txt出力するならこれでOK

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x * dw, w * dw, y * dh, h * dh

for file in os.listdir(input_dir):
    if not file.endswith(".xml"):
        continue
    in_file = open(os.path.join(input_dir, file), encoding='utf-8')
    out_file = open(os.path.join(output_dir, file.replace(".xml", ".txt")), 'w', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    if size is None:
        continue
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(f"{cls_id} {' '.join([str(round(a, 6)) for a in bb])}\n")
