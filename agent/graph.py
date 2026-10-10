from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import AgentNodes


def build_agent_graph(nodes: AgentNodes):
    """
    Xây dựng luồng xử lý của Agent với cơ chế self-correction.

    Luồng:
    START -> retrieve -> generate -> validate -> (conditional)
        - Nếu hợp lệ -> END
        - Nếu không hợp lệ và còn lượt retry -> retrieve (self-correction)
        - Nếu không hợp lệ và hết lượt -> fallback -> END
    """

    workflow = StateGraph(AgentState)

    # Thêm các node
    workflow.add_node("retrieve", nodes.retrieve_documents)
    workflow.add_node("generate", nodes.generate_answer)
    workflow.add_node("validate", nodes.validate_citations)
    workflow.add_node("fallback", nodes.fallback_response)

    # Định nghĩa luồng
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "validate")

    # Conditional edge: quyết định sau khi validate
    def should_continue(state: AgentState) -> str:
        """Quyết định bước tiếp theo dựa trên kết quả validation."""
        validation = state.get("validation_result", {})

        if validation.get("is_valid"):
            return "end"

        if state.get("needs_re_retrieval", False):
            return "re_retrieve"

        return "fallback"

    workflow.add_conditional_edges(
        "validate",
        should_continue,
        {
            "end": END,
            "re_retrieve": "retrieve",  # Self-correction loop
            "fallback": "fallback"
        }
    )

    workflow.add_edge("fallback", END)

    return workflow.compile()