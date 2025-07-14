# NSFW Mosaic Tool (Render Deployable)

AIで陰部（チンコ・膣・アナル）を検出し、モザイクをかける自動処理ツール。400枚以上にも対応可能なバッチ処理構成。

---

## 🔧 機能一覧

- YOLOv8ベースの高精度NSFW部位検出
- Flask UIで操作可能（画像アップ・濃さ調整・プレビュー）
- mosaic_size調整スライダー付き
- 100枚単位の高速バッチ処理
- 自動ZIP化 & ダウンロード機能

---

## 🖥️ ローカル起動方法（開発者向け）

```bash
git clone https://github.com/yourname/nsfw-mosaic-tool.git
cd nsfw-mosaic-tool
pip install -r requirements.txt
python app.py
