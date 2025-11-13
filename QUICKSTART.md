# 🚀 快速部署指南

## 5 分鐘完成部署！

### 📌 步驟 1: 創建 GitHub 倉庫

1. 訪問 https://github.com/new
2. Repository name: `tsmc-news-search`
3. 選擇 **Public**
4. **不要** 勾選 "Initialize this repository with a README"
5. 點擊 "Create repository"

### 📌 步驟 2: 上傳程式碼

**方法 A: 使用自動腳本（推薦）**

雙擊運行 `deploy.bat`（Windows）或 `deploy.sh`（Mac/Linux），然後按照提示操作。

**方法 B: 手動上傳**

```bash
cd C:\Users\user\Desktop\專案\vectorDB
git init
git add .
git commit -m "Initial commit: TSMC news search system"
git remote add origin https://github.com/你的用戶名/tsmc-news-search.git
git branch -M main
git push -u origin main
```

### 📌 步驟 3: 部署到 Streamlit Cloud

1. 訪問 https://streamlit.io/cloud
2. 點擊 "Sign in" → "Continue with GitHub"
3. 點擊 "New app"
4. 填寫資訊：
   - Repository: `你的用戶名/tsmc-news-search`
   - Branch: `main`
   - Main file path: `app.py`
5. 點擊 "Deploy!"

### ✅ 完成！

等待 3-5 分鐘，你會得到一個公開網址：

```
https://你的用戶名-tsmc-news-search.streamlit.app
```

分享給任何人即可使用！

---

## ⚠️ 可能遇到的問題

### 問題 1: Torch 套件太大

如果部署失敗並提示記憶體不足，修改 `requirements.txt`：

```txt
streamlit
chromadb
sentence-transformers
--extra-index-url https://download.pytorch.org/whl/cpu
torch
pandas
openpyxl
numpy
```

然後重新提交：

```bash
git add requirements.txt
git commit -m "Use CPU-only torch"
git push
```

### 問題 2: 首次載入很慢

這是正常的！首次載入需要下載 embedding 模型（約 1-2 分鐘）。之後會使用快取，速度會快很多。

### 問題 3: Git 推送失敗

確保你已經設定 Git 認證：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的郵箱"
```

---

## 📚 詳細說明

查看 `DEPLOYMENT.md` 獲取完整部署文檔和進階設定。
