import os
from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from state import AgentState
from citation_validator import CitationValidator


class AgentNodes:
    """
    Chứa tất cả các node xử lý cho LangGraph.
    """

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        collection_name: str = "legal_documents",
        llm_model: str = "gemini-3.8-flash",
        top_k: int = 5
    ):
        self.llm = ChatGoogleGenerativeAI(
            model=llm_model,
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.top_k = top_k

        # Kết nối Qdrant
        self.qdrant_client = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
            check_compatibility=False,
        )
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=collection_name,
            embedding=self.embeddings
        )

        # Khởi tạo Citation Validator
        self.citation_validator = CitationValidator(self.llm)

    # ================== NODE 1: RETRIEVAL ==================
    def retrieve_documents(self, state: AgentState) -> AgentState:
        """
        Truy xuất tài liệu liên quan từ Qdrant.
        """
        question = state["question"]

        if state.get("needs_re_retrieval") and state.get("validation_result"):
            reason = state["validation_result"].get("reason", "")
            question = f"{question} (Lưu ý: {reason})"

        retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": self.top_k,
                "score_threshold": 0.5
            }
        )

        documents = retriever.invoke(question)

        return {
            **state,
            "documents": documents,
            "needs_re_retrieval": False
        }

    # ================== NODE 2: GENERATION ==================
    def generate_answer(self, state: AgentState) -> AgentState:
        """
        Sinh câu trả lời dựa trên các tài liệu đã truy xuất.
        """
        question = state["question"]
        documents = state["documents"]

        context = "\n\n".join([
            f"[Nguồn {i+1}] (Từ: {doc.metadata.get('source', 'N/A')}):\n{doc.page_content}"
            for i, doc in enumerate(documents)
        ])

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Bạn là trợ lý pháp luật chuyên nghiệp. Nhiệm vụ của bạn là trả lời câu hỏi 
dựa HOÀN TOÀN vào các tài liệu pháp luật được cung cấp.

QUY TẮC NGHIÊM NGẶT:
1. CHỈ sử dụng thông tin từ các tài liệu được cung cấp.
2. KHÔNG bịa đặt hoặc thêm thông tin ngoài tài liệu.
3. Mỗi khẳng định pháp lý PHẢI đi kèm trích dẫn dạng [Nguồn X] hoặc [Điều Y].
4. Nếu không đủ thông tin để trả lời, hãy nói rõ: "Không đủ thông tin trong tài liệu để trả lời."
5. Trình bày rõ ràng, có cấu trúc.
"""),
            ("human", """Câu hỏi: {question}

Các tài liệu pháp luật liên quan:
{context}

Hãy trả lời câu hỏi dựa trên các tài liệu trên, kèm theo trích dẫn nguồn cụ thể.""")
        ])

        chain = prompt | self.llm
        response = chain.invoke({
            "question": question,
            "context": context
        })

        # Gemini trả về content có thể là string hoặc list
        generation = response.content
        if isinstance(generation, list):
            generation = " ".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in generation
            )

        return {
            **state,
            "generation": generation
        }

    # ================== NODE 3: VALIDATION ==================
    def validate_citations(self, state: AgentState) -> AgentState:
        """
        Kiểm tra tính chính xác của trích dẫn trong câu trả lời.
        """
        generation = state["generation"]
        documents = state["documents"]

        validation_result = self.citation_validator.validate(generation, documents)

        needs_re_retrieval = not validation_result["is_valid"]
        retry_count = state.get("retry_count", 0)

        if needs_re_retrieval and retry_count < state.get("max_retries", 2):
            retry_count += 1
        else:
            needs_re_retrieval = False

        return {
            **state,
            "validation_result": validation_result,
            "needs_re_retrieval": needs_re_retrieval,
            "retry_count": retry_count
        }

    # ================== NODE 4: FALLBACK ==================
    def fallback_response(self, state: AgentState) -> AgentState:
        """
        Xử lý khi không thể tạo câu trả lời hợp lệ sau nhiều lần thử.
        """
        fallback_msg = (
            "Xin lỗi, tôi không thể tìm thấy đủ thông tin pháp luật đáng tin cậy "
            "để trả lời câu hỏi này. Vui lòng thử diễn đạt lại câu hỏi hoặc cung cấp "
            "thêm ngữ cảnh."
        )

        if state.get("generation"):
            fallback_msg = (
                f"⚠️ Lưu ý: Câu trả lời sau có thể chưa được kiểm chứng đầy đủ:\n\n"
                f"{state['generation']}\n\n"
                f"Lý do: {state.get('validation_result', {}).get('reason', 'Không xác định')}"
            )

        return {
            **state,
            "generation": fallback_msg,
            "validation_result": {
                "is_valid": False,
                "reason": "Đã sử dụng fallback response",
                "unsupported_claims": []
            }
        }