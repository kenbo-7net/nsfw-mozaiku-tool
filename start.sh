#!/bin/bash

mkdir -p models

if [ ! -f models/yolov8n.pt ]; then
    echo "モデルが見つかりません。自動でダウンロードします..."
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O models/yolov8n.pt
else
    echo "モデルは既に存在しています。"
fi

python app.py
