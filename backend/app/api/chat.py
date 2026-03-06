from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.graph.builder import get_graph
from app.dependencies import get_langfuse
import logging
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Schema cho yêu cầu chat từ người dùng."""
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Schema cho phản hồi từ Agent."""
    reply: str
    session_id: str
    agent_used: Optional[str] = None
    sources: Optional[list] = None
    trace_id: Optional[str] = None


@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Gửi tin nhắn đến Supervisor Agent.
    Supervisor sẽ phân tích intent và điều hướng đến Sub-agent phù hợp.
    """
    try:
        graph = get_graph()
        langfuse_srv = get_langfuse()
        
        # Prepare tracking ID and configuration
        session_id = request.session_id or str(uuid.uuid4())
        user_id = request.user_id or "user-001"
        callbacks = langfuse_srv.get_callback()

        # Prepare initial state
        initial_state = {
            "user_query": request.message,
            "session_id": session_id,
            "user_id": user_id,
            "chat_history": [],
            "context_summary": "",
            "intent": "",
            "sub_queries": [],
            "rag_results": [],
            "rag_query_used": "",
            "rag_crag_retried": False,
            "agent_response": "",
            "agent_used": "",
            "return_to_supervisor": False,
            "error": None,
            "messages": [],
        }

        # Setup runtime config for LangGraph tracking
        run_name = f"chat_{session_id[-8:]}"
        config = {
            "configurable": {"thread_id": session_id},
            "run_name": run_name,
        }
        if callbacks:
            config["callbacks"] = callbacks

        # Invoke Graph with tracing
        result = graph.invoke(initial_state, config=config)

        # Trích xuất trace ID nếu Langfuse đang bật
        trace_id = callbacks[0].trace_id if callbacks and hasattr(callbacks[0], "trace_id") else None

        return ChatResponse(
            reply=result.get("agent_response", "Không có phản hồi."),
            session_id=session_id,
            agent_used=result.get("agent_used", "unknown"),
            trace_id=trace_id,
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ChatResponse(
            reply=f"Xin lỗi, có lỗi xảy ra: {str(e)}",
            session_id=request.session_id or "default-session",
            agent_used="error",
        )


@router.get("/sessions")
async def list_sessions():
    """Lấy danh sách các phiên chat."""
    # TODO: Kết nối SQLite
    return {"sessions": []}


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str):
    """Lấy lịch sử tin nhắn của một phiên chat."""
    # TODO: Kết nối SQLite
    return {"session_id": session_id, "messages": []}
