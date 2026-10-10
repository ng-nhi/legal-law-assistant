from typing import TypedDict, List, Annotated
from langchain_core.documents import Document
import operator

class AgentState(TypedDict):
    """
    Trạng thái của Agent trong quá trình xử lý.
    """
    question: str                          # Câu hỏi đầu vào của người dùng
    documents: List[Document]              # Các tài liệu được truy xuất
    generation: str                        # Câu trả lời được sinh ra
    citations: List[str]                   # Danh sách các trích dẫn được sử dụng
    validation_result: dict                # Kết quả kiểm tra trích dẫn (is_valid, reason)
    retry_count: int                       # Số lần thử lại (cho self-correction)
    max_retries: int                       # Số lần thử lại tối đa
    needs_re_retrieval: bool               # Cờ báo hiệu cần truy xuất lại