# 韓文字典查詢系統

Flask + pandas 字典網站。資料放在同目錄的 `korean_dictionary_template.csv`。

## 本機執行

安裝 Python 3.10 以上版本後，在這個資料夾執行：

```bash
python -m pip install -r requirements.txt
python app.py
```

瀏覽 http://127.0.0.1:5000

## 公開部署（GitHub + Render）

GitHub 負責保存原始碼；Render 負責執行 Flask 並提供公開網址。GitHub Pages 不能執行 Flask 後端。

1. 在 GitHub 建立新 repository，例如 `korean-dict-app`。
2. 將本資料夾中的 `app.py`、`korean_dictionary_template.csv`、`requirements.txt`、`render.yaml` 和 `.gitignore` 上傳到 repository 根目錄。CSV 會隨公開程式碼公開，請勿放入私人資料。
3. 到 Render 建立 Web Service，連結 GitHub 帳號與 repository。Render 會依 `render.yaml` 安裝套件並用 Gunicorn 啟動。
4. 部署完成後，使用 Render 提供的 `onrender.com` 網址分享網站。免費服務可能在閒置後休眠，第一次開啟會較慢。

之後更新字典時，修改 CSV 並推送到 GitHub；Render 會自動重新部署。
