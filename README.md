# 🟡 NSFW Mosaic Tool – AI局部モザイク自動化ツール（Render対応）

YOLOv8を用いて局部（チンコ・膣・アナル）のみを高精度に検出し、自動でモザイク処理を行うWebツールです。最大100枚までの画像をまとめて処理し、ZIPで一括ダウンロードが可能。Renderによりブラウザ上で簡単に利用できます。

---

## 🔧 機能一覧

- ✅ YOLOv8モデルによるNSFW部位検出（genital.pt 対応）
- ✅ モザイクの濃さ（サイズ）をスライダーで調整可能
- ✅ 100枚までの画像を一括処理（PNG/JPG/JPEG対応）
- ✅ ZIP自動生成＆ダウンロード機能付き
- ✅ Webブラウザから直接操作可能（Flaskベース）
- ✅ Render にワンクリックでデプロイ可能

---

## 🚀 デモサイト（Render公開URL）

👉 https://your-render-subdomain.onrender.com

> ※ ご自身でデプロイするには以下の「デプロイ方法」をご覧ください。

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kenbo-7net/nsfw-mozaiku-tool)

---

## 🛠️ デプロイ方法（Render またはローカル）

### 🔹 Render で公開（推奨）

1. genital.pt を以下のように配置してください：


2. 上の Render ボタンをクリックし、GitHubアカウントと連携してデプロイ

3. `Start Command`：`python app.py`  
   `Build Command`：`pip install -r requirements.txt`  
   `Python Version`：`3.10.12`

---

### 🔹 ローカル環境で実行（開発者向け）

```bash
git clone https://github.com/kenbo-7net/nsfw-mozaiku-tool.git
cd nsfw-mozaiku-tool

# genital.pt を yolo_models/ に配置
pip install -r requirements.txt
python app.py
nsfw-mozaiku-tool/
├── app.py               # Flask アプリ本体
├── nsfw_mosaic.py       # YOLO検出＋モザイク処理
├── utils.py             # 補助関数
├── batch_zipper.py      # ZIP生成ロジック
├── templates/
│   └── index.html       # フロントエンドUI
├── yolo_models/
│   └── genital.pt       # 学習済みYOLOv8モデル
├── requirements.txt     # 必要パッケージ一覧
├── render.yaml          # Render用設定
└── README.md            # このファイル

---

必要に応じて、上記を `README.md` にそのままコピペすれば即使えます。  
アイコンやデザインはすべて日本語に最適化しており、RenderでもGitHubでも完璧に表示されます。

---

### ✅ 次のステップおすすめ：

- `LICENSE` ファイル追加（MITなど）
- `genital.pt` モデル入手ガイド（models/README.md）
- `public/sample_xxx.png` の実画像アップ

これらが揃えば、完全に共有可能なNSFWツールとして公開レベルに仕上がります。必要なら追加もサポートします。
