"""
Script nạp data pháp luật mẫu vào Qdrant để test Agent.
Chạy: python seed_data.py
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
warnings.filterwarnings("ignore", category=FutureWarning)

import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

COLLECTION_NAME = "legal_documents"
VECTOR_SIZE = 3072   # ← Gemini gemini-embedding-001


SAMPLE_DOCS = [
    Document(
        page_content=(
            "Điều 173. Tội trộm cắp tài sản. "
            "1. Người nào trộm cắp tài sản của người khác trị giá từ 2.000.000 đồng "
            "đến dưới 50.000.000 đồng thì bị phạt cải tạo không giam giữ đến 03 năm "
            "hoặc phạt tù từ 06 tháng đến 03 năm. "
            "2. Phạm tội thuộc một trong các trường hợp sau đây thì bị phạt tù từ "
            "02 năm đến 07 năm: a) Có tổ chức; b) Có tính chất chuyên nghiệp; "
            "c) Tài sản trị giá từ 50.000.000 đồng đến dưới 200.000.000 đồng."
        ),
        metadata={
            "source": "Bộ luật Hình sự 2015 (sửa đổi 2017)",
            "article": "Điều 173",
            "topic": "Tội trộm cắp tài sản"
        }
    ),
    Document(
        page_content=(
            "Điều 174. Tội lừa đảo chiếm đoạt tài sản. "
            "1. Người nào bằng thủ đoạn gian dối chiếm đoạt tài sản của người khác "
            "trị giá từ 2.000.000 đồng đến dưới 50.000.000 đồng thì bị phạt cải tạo "
            "không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm."
        ),
        metadata={
            "source": "Bộ luật Hình sự 2015 (sửa đổi 2017)",
            "article": "Điều 174",
            "topic": "Tội lừa đảo chiếm đoạt tài sản"
        }
    ),
    Document(
        page_content=(
            "Điều 175. Tội lạm dụng tín nhiệm chiếm đoạt tài sản. "
            "1. Người nào thực hiện một trong các hành vi sau đây chiếm đoạt tài sản "
            "của người khác trị giá từ 4.000.000 đồng đến dưới 50.000.000 đồng thì "
            "bị phạt cải tạo không giam giữ đến 03 năm hoặc phạt tù từ 06 tháng đến 03 năm."
        ),
        metadata={
            "source": "Bộ luật Hình sự 2015 (sửa đổi 2017)",
            "article": "Điều 175",
            "topic": "Tội lạm dụng tín nhiệm chiếm đoạt tài sản"
        }
    ),
    Document(
        page_content=(
            "Điều 611. Thời điểm phát sinh quyền và nghĩa vụ của người thừa kế. "
            "1. Thời điểm phát sinh quyền và nghĩa vụ của người thừa kế là thời điểm "
            "mở thừa kế. 2. Khi di sản được chia thừa kế thì quyền và nghĩa vụ của "
            "người thừa kế được xác lập tương ứng với phần di sản được hưởng."
        ),
        metadata={
            "source": "Bộ luật Dân sự 2015",
            "article": "Điều 611",
            "topic": "Thừa kế"
        }
    ),
]


def main():
    print("=" * 60)
    print("🌱 SEED DATA VÀO QDRANT (Google Gemini 3072 chiều)")
    print("=" * 60)

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Chưa có GOOGLE_API_KEY trong .env")
        return

    # Kết nối Qdrant
    client = QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", 6333)),
        check_compatibility=False,
    )

    # Xóa collection cũ nếu tồn tại
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"⚠️  Đã xóa collection cũ '{COLLECTION_NAME}'")
    except Exception:
        print(f"ℹ️  Collection '{COLLECTION_NAME}' chưa tồn tại")

    # Tạo collection mới với 3072 chiều
    print(f"📦 Tạo collection '{COLLECTION_NAME}' với {VECTOR_SIZE} chiều...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

    # Nạp data
    print(f"📥 Đang embed và nạp {len(SAMPLE_DOCS)} tài liệu...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
    vector_store.add_documents(SAMPLE_DOCS)

    # Verify
    count = client.count(collection_name=COLLECTION_NAME).count
    print(f"✅ Đã nạp {count} tài liệu")

    # Test tìm kiếm
    print("\n🔍 Test tìm kiếm 'tội trộm cắp bị phạt gì':")
    results = vector_store.similarity_search("tội trộm cắp bị phạt gì", k=2)
    for i, doc in enumerate(results, 1):
        print(f"   {i}. {doc.metadata.get('article')} - {doc.metadata.get('topic')}")

    print("\n" + "=" * 60)
    print("✅ HOÀN THÀNH — Giờ chạy: python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()