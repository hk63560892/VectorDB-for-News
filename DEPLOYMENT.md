# 部署到 Streamlit Community Cloud 指南

## 📋 前置準備

你的專案已經準備好部署了！以下是需要上傳到 GitHub 的文件：

```
vectorDB/
├── app.py                      # Streamlit 應用程式
├── ingest_data.py              # 資料匯入腳本
├── requirements.txt            # Python 依賴套件
├── .gitignore                  # Git 忽略文件
├── README.md                   # 專案說明
├── 台積電新聞整理.xlsx          # 資料來源
└── vector_storage/             # 向量資料庫（1.2MB）
    ├── chroma.sqlite3
    └── [其他資料庫文件]
```

## 🚀 部署步驟

### 步驟 1: 創建 GitHub 倉庫

1. 訪問 https://github.com 並登入
2. 點擊右上角的 "+" → "New repository"
3. 填寫倉庫資訊：
   - Repository name: `tsmc-news-search`（或你喜歡的名稱）
   - Description: `台積電新聞檢索系統 - 使用向量資料庫的語意搜索`
   - 選擇 "Public"（Streamlit Cloud 免費版需要公開倉庫）
   - ✅ 不要勾選 "Initialize this repository with a README"
4. 點擊 "Create repository"

### 步驟 2: 上傳專案到 GitHub

打開 Git Bash 或 Terminal，執行以下命令：

```bash
# 進入專案目錄
cd C:\Users\user\Desktop\專案\vectorDB

# 初始化 Git 倉庫
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: TSMC news search system with vector database"

# 連接到 GitHub（替換成你的 GitHub 用戶名和倉庫名）
git remote add origin https://github.com/你的用戶名/tsmc-news-search.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 步驟 3: 部署到 Streamlit Cloud

1. **訪問 Streamlit Cloud**
   - 前往 https://streamlit.io/cloud
   - 點擊 "Sign in" → 選擇 "Continue with GitHub"

2. **創建新應用**
   - 點擊 "New app"
   - 選擇你的 GitHub 倉庫：`你的用戶名/tsmc-news-search`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: 選擇你想要的網址（例如：`tsmc-news-search`）

3. **進階設定（可選）**
   - Python version: 選擇 `3.11` 或 `3.10`
   - 如果需要，可以設定環境變數

4. **部署**
   - 點擊 "Deploy!"
   - 等待 3-5 分鐘讓 Streamlit Cloud 安裝依賴並啟動應用

5. **完成！**
   - 你會得到一個公開網址，例如：
     `https://你的用戶名-tsmc-news-search.streamlit.app`
   - 分享這個網址給任何人，他們就能使用你的應用！

## 📝 重要注意事項

### 關於 Torch 套件

Streamlit Cloud 的資源有限，完整版的 `torch` 可能太大。如果部署失敗，需要修改 `requirements.txt`：

```txt
streamlit==1.47.0
chromadb==1.3.4
sentence-transformers==4.1.0
torch==2.7.1+cpu  # 使用 CPU 版本
pandas==2.2.3
openpyxl==3.1.2
numpy==2.2.3
```

或者使用更輕量的版本：

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

### 向量資料庫

- ✅ 已包含預先建立的向量資料庫（1.2MB）
- ✅ 部署後立即可用，無需重新建立
- 如果需要更新資料，在本地運行 `python ingest_data.py`，然後推送到 GitHub

### 資料更新

如果你更新了台積電新聞資料：

```bash
# 1. 在本地更新 Excel 文件
# 2. 重新建立向量資料庫
python ingest_data.py

# 3. 提交並推送到 GitHub
git add .
git commit -m "Update news data"
git push

# 4. Streamlit Cloud 會自動重新部署
```

## 🔧 故障排除

### 部署失敗：記憶體不足

如果遇到記憶體問題，可以：
1. 使用 CPU 版本的 PyTorch（見上方）
2. 減少向量資料庫大小（只保留最新的新聞）

### 應用啟動緩慢

第一次載入 Sentence Transformer 模型可能需要 1-2 分鐘，這是正常的。後續訪問會使用快取，速度會快很多。

### 無法訪問資料庫

確保 `vector_storage/` 資料夾已經上傳到 GitHub：
```bash
git ls-files | grep vector_storage
```

## 🎉 完成後

分享你的應用網址給任何人：
```
https://你的用戶名-tsmc-news-search.streamlit.app
```

他們無需安裝任何東西，直接在瀏覽器中使用！

## 💡 額外功能（可選）

### 添加密碼保護

在 `app.py` 開頭添加：

```python
import streamlit as st

# 簡單的密碼保護
def check_password():
    def password_entered():
        if st.session_state["password"] == "your_password_here":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "請輸入密碼", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "請輸入密碼", type="password", on_change=password_entered, key="password"
        )
        st.error("密碼錯誤")
        return False
    else:
        return True

if not check_password():
    st.stop()

# 其餘的應用程式代碼...
```

### 使用 Streamlit Secrets

在 Streamlit Cloud 設定中添加 secrets，避免硬編碼敏感資訊。
