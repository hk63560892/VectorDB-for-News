import pandas as pd
from sentence_transformers import SentenceTransformer
import torch
import chromadb
from tqdm import tqdm
import os

class VectorDBManager:
    """
    一個用於處理文本向量化並存儲到 ChromaDB 的管理器。
    """
    def __init__(self, db_path="vector_storage", collection_name="news_collection"):
        """
        初始化 VectorDBManager。

        :param db_path: ChromaDB 數據庫的存儲路徑。
        :param collection_name: 要操作的集合名稱。
        """
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def _load_embedding_model(self, model_name):
        """
        加載指定的句子轉換器模型。
        注意：請確保已清除舊版本緩存以使用最新版本。
        """
        print(f"正在加載嵌入模型: {model_name}...")
        print(f"使用設備: {self.device}")
        self.model = SentenceTransformer(model_name, device=self.device)
        print("模型加載完成。")

    def _read_data(self, file_path):
        """
        從 Excel 文件中讀取數據，合併 SUBJECT 和 CONTENT，並保留 metadata。
        """
        print(f"正在從 {file_path} 讀取資料...")
        try:
            df = pd.read_excel(file_path)

            # 檢查必要欄位
            required_columns = ['SUBJECT', 'CONTENT', 'NEWS_DATE', 'NEWS_TYPE']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"錯誤：缺少必要欄位 {missing_columns}。")

            # 移除 SUBJECT 或 CONTENT 為空的資料
            df.dropna(subset=['SUBJECT', 'CONTENT'], how='all', inplace=True)

            # 填充空值為空字串
            df['SUBJECT'] = df['SUBJECT'].fillna('')
            df['CONTENT'] = df['CONTENT'].fillna('')
            df['NEWS_DATE'] = df['NEWS_DATE'].fillna('')
            df['NEWS_TYPE'] = df['NEWS_TYPE'].fillna('')

            # 合併 SUBJECT 和 CONTENT
            df['combined_text'] = df['SUBJECT'] + '\n\n' + df['CONTENT']

            print(f"成功讀取 {len(df)} 筆有效資料。")
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"錯誤：找不到檔案 {file_path}。請檢查路徑是否正確。")
        except Exception as e:
            raise e

    def process_and_store(self, file_path, model_name):
        """
        處理整個流程：讀取數據、生成嵌入、存儲到 ChromaDB（包含 metadata）。
        """
        self._load_embedding_model(model_name)
        df = self._read_data(file_path)

        print("正在生成文本嵌入並存入向量資料庫...")
        print("使用 normalize_embeddings=True（自動處理 batch）")

        # 提取合併後的文本
        documents = df['combined_text'].tolist()

        # SentenceTransformer 會自動處理 batch，不需要手動分批
        embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        # 分批寫入 ChromaDB（包含 metadata）
        batch_size = 1000
        for i in tqdm(range(0, len(documents), batch_size), desc="寫入資料庫"):
            batch_docs = documents[i:i+batch_size]
            batch_embeddings = embeddings[i:i+batch_size]
            ids = [f"doc_{j}" for j in range(i, i + len(batch_docs))]

            # 準備 metadata
            batch_metadata = []
            for j in range(i, i + len(batch_docs)):
                metadata = {
                    'news_date': str(df.iloc[j]['NEWS_DATE']),
                    'news_type': str(df.iloc[j]['NEWS_TYPE']),
                    'subject': str(df.iloc[j]['SUBJECT'])
                }
                batch_metadata.append(metadata)

            self.collection.add(
                embeddings=batch_embeddings.tolist(),
                documents=batch_docs,
                ids=ids,
                metadatas=batch_metadata
            )

        print("\n所有資料已成功向量化並存儲到 ChromaDB。")
        print(f"資料庫位置: {os.path.abspath(self.db_path)}")
        print(f"集合 '{self.collection.name}' 中現在有 {self.collection.count()} 筆資料。")


if __name__ == '__main__':
    # --- 使用者設定 ---
    # 1. 嵌入模型
    MODEL_NAME = "maidalun1020/bce-embedding-base_v1"

    # 2. Excel 檔案的絕對路徑（使用相對路徑以支援部署）
    EXCEL_FILE_PATH = os.path.join(os.path.dirname(__file__), "台積電新聞整理.xlsx")

    # 3. 資料庫存儲路徑和集合名稱
    DB_STORAGE_PATH = "vector_storage"
    COLLECTION_NAME = "tsmc_news"
    # --- 設定結束 ---

    print("=" * 60)
    print("向量化設定：")
    print("- 將 SUBJECT 和 CONTENT 合併後進行向量化")
    print("- 保留 NEWS_DATE 和 NEWS_TYPE 作為 metadata")
    print("=" * 60)

    try:
        db_manager = VectorDBManager(db_path=DB_STORAGE_PATH, collection_name=COLLECTION_NAME)
        db_manager.process_and_store(
            file_path=EXCEL_FILE_PATH,
            model_name=MODEL_NAME
        )

    except (FileNotFoundError, ValueError) as e:
        print(e)
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")