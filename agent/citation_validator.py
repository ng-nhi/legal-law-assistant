"""
Citation Validator - Kiểm tra tính chính xác của nguồn trích dẫn.
Issue #5: Xây dựng cơ chế kiểm tra tính chính xác của nguồn trích dẫn.
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import re
from typing import List, Dict
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


# ================== SCHEMA ==================
class CitationValidation(BaseModel):
    """Schema cho kết quả kiểm tra trích dẫn."""
    is_valid: bool = Field(
        description="True nếu câu trả lời được hỗ trợ hoàn toàn bởi các trích dẫn"
    )
    reason: str = Field(
        description="Lý do chi tiết (bằng tiếng Việt) giải thích kết quả"
    )
    unsupported_claims: List[str] = Field(
        default_factory=list,
        description="Danh sách các khẳng định không được hỗ trợ bởi nguồn"
    )


# ================== VALIDATOR ==================
class CitationValidator:
    """
    Cơ chế kiểm tra tính chính xác của nguồn trích dẫn.
    Đối chiếu câu trả lời với các tài liệu gốc để phát hiện ảo giác (hallucination).
    """

    def __init__(self, llm: ChatGoogleGenerativeAI = None):
        # Nếu không truyền llm, tự tạo mới
        self.llm = llm or ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.validator_chain = self._build_validator_chain()

    def _build_validator_chain(self):
        """Xây dựng chain kiểm tra trích dẫn."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Bạn là một chuyên gia kiểm tra tính chính xác của trích dẫn pháp luật.
Nhiệm vụ của bạn là đối chiếu câu trả lời với các tài liệu nguồn được cung cấp.

Quy tắc kiểm tra:
1. Mọi khẳng định pháp lý trong câu trả lời PHẢI được hỗ trợ bởi ít nhất một tài liệu nguồn.
2. Nếu câu trả lời chứa thông tin không có trong nguồn -> KHÔNG HỢP LỆ.
3. Nếu trích dẫn sai điều luật, sai số ký hiệu -> KHÔNG HỢP LỆ.
4. Nếu câu trả lời diễn giải sai ý của điều luật -> KHÔNG HỢP LỆ.
5. Nếu câu trả lời nói "không đủ thông tin" và điều đó đúng với nguồn -> HỢP LỆ.

Trả về kết quả dưới dạng JSON với các trường:
- is_valid: boolean
- reason: string (giải thích bằng tiếng Việt)
- unsupported_claims: list[string] (các khẳng định không được hỗ trợ)
"""),
            ("human", """Câu trả lời của hệ thống:
{generation}

Các tài liệu nguồn được trích dẫn:
{documents}

Hãy kiểm tra tính chính xác của các trích dẫn trong câu trả lời.""")
        ])

        return prompt | self.llm.with_structured_output(CitationValidation)

    def validate(self, generation: str, documents: List[Document]) -> Dict:
        """Kiểm tra tính hợp lệ của trích dẫn."""
        # Nếu không có tài liệu nào được trích dẫn -> không hợp lệ
        if not documents:
            return {
                "is_valid": False,
                "reason": "Không có tài liệu nguồn nào được trích dẫn.",
                "unsupported_claims": [generation]
            }

        # Format documents thành text
        docs_text = "\n\n".join([
            f"[Nguồn {i + 1}]: {doc.metadata.get('source', 'Không rõ')}\n"
            f"Nội dung: {doc.page_content}"
            for i, doc in enumerate(documents)
        ])

        try:
            result: CitationValidation = self.validator_chain.invoke({
                "generation": generation,
                "documents": docs_text
            })
            return {
                "is_valid": result.is_valid,
                "reason": result.reason,
                "unsupported_claims": result.unsupported_claims
            }
        except Exception as e:
            return {
                "is_valid": False,
                "reason": f"Lỗi khi kiểm tra trích dẫn: {str(e)}",
                "unsupported_claims": []
            }

    @staticmethod
    def extract_citations(generation: str) -> List[str]:
        """Trích xuất các trích dẫn từ câu trả lời."""
        patterns = [
            r'\[\d+\]',
            r'\[Điều \d+\]',
            r'\[Khoản \d+, Điều \d+\]',
        ]
        citations = []
        for pattern in patterns:
            citations.extend(re.findall(pattern, generation))
        return list(set(citations))