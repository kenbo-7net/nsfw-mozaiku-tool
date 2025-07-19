# NSFW Mosaic Tool (AIモザイク処理ツール)

画像内の性的部位（ペニス・膣・アナル）をAIで検出し、自動的にモザイク処理を施すWebツールです。複数画像に対応し、処理ログのCSV出力やSlack通知にも対応。

---

## 🖼 主な機能

- ✅ ペニス・膣・アナルの3クラスのみを正確に検出
- ✅ YOLOv8 + 自前学習モデルによる高精度モザイク処理
- ✅ 最大100枚一括ドロップ対応
- ✅ モザイク後の画像一覧表示・モーダル拡大・削除
- ✅ 処理中アニメーション（ローディングUI）
- ✅ ZIP一括ダウンロード
- ✅ ファイル名ルール指定
- ✅ 処理ログ（CSV形式）出力
- ✅ Slack通知（Webhook対応）

---

## 🛠 使用方法

1. 任意の画像をドラッグ＆ドロップ
2. 処理が自動で開始され、完了後に画像一覧が表示されます
3. ZIPで一括ダウンロードも可能

---

## 🚀 デプロイ構成

- Render（無料Webデプロイ対応）
- Flask（Python）
- YOLOv8 + genital.pt（Git LFS管理）

---

## 📦 セットアップ方法（開発者向け）

```bash
git clone https://github.com/kenbo-7net/nsfw-mozaiku-tool.git
cd nsfw-mozaiku-tool

# LFSセットアップ（ptファイル用）
git lfs install
git lfs pull

# 仮想環境構築と依存関係
python -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# 起動
python app.py
