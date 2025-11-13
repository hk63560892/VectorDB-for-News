import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import torch
import os

# --- 設定 (必須與 ingest_data.py 中的設定一致) ---
MODEL_NAME = "maidalun1020/bce-embedding-base_v1"
DB_STORAGE_PATH = os.path.join(os.path.dirname(__file__), "vector_storage")
COLLECTION_NAME = "tsmc_news"

# --- Streamlit 應用程式 ---

st.set_page_config(page_title="新聞檢索系統", page_icon="📰")
st.title("📰 新聞檢索系統")
st.caption(f"使用 {MODEL_NAME} 模型進行語意搜索")

# --- 快取資源 ---
# 使用 Streamlit 的快取功能，避免重複加載模型和資料庫，加快反應速度
@st.cache_resource
def load_model():
    """加載並快取句子轉換器模型"""
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        return SentenceTransformer(MODEL_NAME, device=device)
    except Exception as e:
        st.error(f"加載模型失敗: {e}")
        return None

@st.cache_resource
def get_collection():
    """連接並快取 ChromaDB 集合"""
    try:
        if not os.path.exists(DB_STORAGE_PATH):
            return None # 資料庫不存在
        client = chromadb.PersistentClient(path=DB_STORAGE_PATH)
        return client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        st.error(f"連接資料庫失敗: {e}")
        return None

# --- 主應用程式邏輯 ---
model = load_model()
collection = get_collection()

if model is None or collection is None:
    st.error("系統初始化失敗，無法提供服務。")
    if not os.path.exists(DB_STORAGE_PATH):
        st.warning(f"找不到向量資料庫 ({DB_STORAGE_PATH})。請先執行 `ingest_data.py` 來建立資料庫。")
else:
    # --- 使用者輸入 ---
    query = st.text_input("請輸入您想查詢的關鍵字或句子：", placeholder="例如：美國設廠進度")

    if query:
        # --- 執行檢索 ---
        with st.spinner("正在進行語意搜索..."):
            try:
                # 1. 將查詢文字轉換為向量（必須 normalize！）
                query_embedding = model.encode(
                    query,
                    normalize_embeddings=True
                ).tolist()

                # 2. 在 ChromaDB 中查詢候選資料（獲取較多結果以便篩選）
                # 先獲取較多的結果，之後根據距離閾值篩選
                max_candidates = 30
                total_count = collection.count()
                n_results = min(max_candidates, total_count) if total_count > 0 else 1

                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results
                )

                # 3. 根據距離閾值篩選結果
                DISTANCE_THRESHOLD = 1.3  # 距離閾值
                MAX_RESULTS = 10  # 最多顯示的結果數量

                all_documents = results.get('documents', [[]])[0]
                all_distances = results.get('distances', [[]])[0]
                all_metadatas = results.get('metadatas', [[]])[0]

                # 篩選距離小於閾值的結果
                filtered_results = [
                    (doc, dist, meta)
                    for doc, dist, meta in zip(all_documents, all_distances, all_metadatas)
                    if dist < DISTANCE_THRESHOLD
                ]

                # 如果結果超過 MAX_RESULTS，只取前 MAX_RESULTS 筆
                filtered_results = filtered_results[:MAX_RESULTS]

                # 4. 顯示結果
                st.subheader(f"檢索結果（距離 < {DISTANCE_THRESHOLD}）：")

                if not filtered_results:
                    st.info(f"找不到距離小於 {DISTANCE_THRESHOLD} 的相關資料。請嘗試其他關鍵字。")
                else:
                    st.success(f"找到 {len(filtered_results)} 筆相關結果")
                    for i, (doc, dist, metadata) in enumerate(filtered_results):
                        # 對於 normalized vectors，L2 距離轉換為餘弦相似度
                        # cosine_similarity = 1 - (L2_distance^2 / 2)
                        similarity = 1 - (dist ** 2 / 2)

                        st.markdown(f"### 結果 {i+1}")

                        # 顯示標題（從 metadata 取得）
                        subject = metadata.get('subject', '無標題')
                        st.markdown(f"**📰 {subject}**")

                        # 顯示日期和類型
                        news_date = metadata.get('news_date', '未知日期')
                        news_type = metadata.get('news_type', '未知類型')
                        st.markdown(f"🗓️ **日期**: {news_date} | 🏷️ **類型**: {news_type}")

                        # 顯示相似度
                        st.markdown(f"📊 **相似度**: {similarity:.4f} (距離: {dist:.4f})")

                        # 顯示完整內容
                        with st.expander("查看完整內容", expanded=True):
                            st.markdown(doc)

                        st.divider()

            except Exception as e:
                st.error(f"檢索過程中發生錯誤: {e}")

# --- 頁腳 ---
st.markdown("---")
st.markdown("這是一個使用 Streamlit、ChromaDB 和 Sentence Transformers 建立的語意搜索應用程式。")
