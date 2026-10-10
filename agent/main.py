"""
Entry point để test toàn bộ Agent.
Chạy: python main.py
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*allowed_objects.*")
import os
from dotenv import load_dotenv

load_dotenv()

from nodes import AgentNodes
from graph import build_agent_graph


def main():
    print("=" * 60)
    print("🚀 LEGAL ASSISTANT AGENT - DEMO")
    print("=" * 60)

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Chưa có GOOGLE_API_KEY trong file .env")
        return
    # Khởi tạo nodes & graph
    nodes = AgentNodes(
        qdrant_host=os.getenv("QDRANT_HOST", "localhost"),
        qdrant_port=int(os.getenv("QDRANT_PORT", 6333)),
        collection_name=os.getenv("QDRANT_COLLECTION", "legal_documents"),
    )

    graph = build_agent_graph(nodes)

    # Test với câu hỏi mẫu
    question = "Hình phạt cho tội trộm cắp tài sản là gì?"

    initial_state = {
        "question": question,
        "documents": [],
        "generation": "",
        "citations": [],
        "validation_result": {},
        "retry_count": 0,
        "max_retries": 2,
        "needs_re_retrieval": False,
    }

    print(f"\n❓ Câu hỏi: {question}\n")
    result = graph.invoke(initial_state)

    print(f"💬 Câu trả lời:\n{result['generation']}\n")
    print(f"✅ Validation: {result['validation_result'].get('is_valid')}")
    print(f"🔄 Retry: {result['retry_count']}")


if __name__ == "__main__":
    main()