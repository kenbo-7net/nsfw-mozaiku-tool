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

