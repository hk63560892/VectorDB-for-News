# 台積電新聞檢索系統

這是一個使用向量資料庫和語意搜索技術的新聞檢索系統，可以快速找到與查詢相關的台積電新聞內容。

🌐 **線上版本**: [部署到 Streamlit Cloud](https://streamlit.io/cloud) - 任何人都可以使用！

## ✨ 功能特色

- 🔍 **智能語意搜索**：使用 BCE embedding 模型理解查詢意圖
- 📊 **相關度篩選**：只顯示距離 < 1.3 的高相關結果（最多 10 筆）
- 📰 **完整資訊**：顯示標題、日期、類型和完整內容
- 🚀 **快速響應**：使用 ChromaDB 向量資料庫加速檢索
- ☁️ **雲端部署**：支援部署到 Streamlit Community Cloud

## 系統架構

- **ChromaDB**: 向量資料庫，用於存儲新聞的向量表示
- **Sentence Transformers**: 使用 `maidalun1020/bce-embedding-base_v1` 模型進行文本向量化
- **Streamlit**: 提供網頁介面

## 專案結構

```
vectorDB/
├── ingest_data.py      # 資料匯入腳本（建立向量資料庫）
├── app.py              # Streamlit 網頁應用程式
├── vector_storage/     # 向量資料庫存儲目錄（自動生成）
└── README.md           # 本說明文件
```

## 安裝依賴

```bash
pip install streamlit chromadb sentence-transformers torch pandas openpyxl
```

## 使用步驟

### 步驟 1: 建立向量資料庫（首次使用）

在首次使用或需要更新資料時，執行以下命令：

```bash
cd C:\Users\user\Desktop\專案\vectorDB
python ingest_data.py
```

**功能說明：**
- 從 Excel 文件讀取台積電新聞資料
- 將文本轉換為向量（embedding）
- 存儲到 ChromaDB 向量資料庫

**預設設定：**
- Excel 檔案路徑: `C:\Users\user\Downloads\台積電新聞整理.xlsx`
- 向量化欄位: `CONTENT`
- 資料庫路徑: `vector_storage`
- 集合名稱: `tsmc_news`

### 步驟 2: 啟動網頁應用

```bash
cd C:\Users\user\Desktop\專案\vectorDB
streamlit run app.py
```

或

```bash
python -m streamlit run app.py
```

啟動後會顯示：
```
Local URL: http://localhost:8502
Network URL: http://172.20.10.10:8502
```

在瀏覽器中打開上述網址即可使用。

## 使用方式

1. 在網頁介面的輸入框中輸入關鍵字或問題
   - 例如：「美國設廠進度」、「先進製程」、「技術發展」
2. 系統會返回最相關的 5 筆新聞內容
3. 每筆結果會顯示相似度分數和完整內容

## 配置說明

### 修改 ingest_data.py 設定

如果需要修改資料來源或設定，請編輯 `ingest_data.py` 的以下部分：

```python
# 1. 嵌入模型
MODEL_NAME = "maidalun1020/bce-embedding-base_v1"

# 2. Excel 檔案的絕對路徑
EXCEL_FILE_PATH = r"C:\Users\user\Downloads\台積電新聞整理.xlsx"

# 3. 要向量化的欄位名稱
COLUMN_TO_VECTORIZE = "CONTENT"

# 4. 資料庫存儲路徑和集合名稱
DB_STORAGE_PATH = "vector_storage"
COLLECTION_NAME = "tsmc_news"
```

### 修改 app.py 設定

確保 `app.py` 中的設定與 `ingest_data.py` 一致：

```python
MODEL_NAME = "maidalun1020/bce-embedding-base_v1"
DB_STORAGE_PATH = f"C:/Users/user/Desktop/專案/vectorDB/vector_storage"
COLLECTION_NAME = "tsmc_news"
```

## 常見問題

### Q: 無法啟動 Streamlit？
A: 確認已安裝 streamlit：`pip install streamlit`

### Q: 找不到資料庫？
A: 先執行 `python ingest_data.py` 建立向量資料庫

### Q: 找不到 'content' 欄位？
A: 檢查 Excel 文件的欄位名稱，確保 `COLUMN_TO_VECTORIZE` 設定正確（注意大小寫）

### Q: 如何更新資料庫？
A: 更新 Excel 文件後，重新執行 `python ingest_data.py`

### Q: 如何停止應用程式？
A: 在終端機按 `Ctrl + C`

## 技術細節

- **向量化技術**: 使用 BCE (Bilingual Contextualized Embeddings) 模型
- **相似度計算**: 使用餘弦相似度（Cosine Similarity）
- **GPU 加速**: 自動偵測 CUDA，有 GPU 時會自動使用
- **正規化**: 所有向量都經過正規化處理以提高搜索準確度

## 系統需求

- Python 3.8+
- 8GB+ RAM（建議）
- CUDA 支援的 GPU（可選，可加速運算）
