"""
Sales / Product Agent Node
==========================
Sub-agent chuyên tra cứu thông tin sản phẩm và tư vấn bán hàng.
"""
import logging
from app.graph.state import AgentState

logger = logging.getLogger(__name__)

def sales_agent_node(state: AgentState) -> dict:
    """
    Xử lý các truy vấn liên quan đến sản phẩm, mua bán, giá cả.
    Hiện tại sử dụng mock data, tương lai sẽ kết nối Product DB.
    """
    query = state.get("user_query", "").lower()
    
    # Mock logic
    if "sữa hạt" in query or "macca" in query:
        response = "Sản phẩm Sữa hạt Macca hiện đang có giá 50,000đ/chai 500ml. Đang có chương trình freeship cho đơn từ 3 chai. Bạn muốn đặt mua không?"
    else:
        response = "Hiện tại kho dữ liệu sản phẩm của chúng tôi đang được cập nhật. Bạn vui lòng cung cấp thêm thông tin sản phẩm nhé."

    return {
        "agent_response": response,
        "agent_used": "sales_agent",
        "return_to_supervisor": True,
    }
