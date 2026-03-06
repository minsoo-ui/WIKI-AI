# Phase 06: Observability (LangFuse Integration)

## Objective
Tích hợp LangFuse SDK để trace toàn bộ luồng hoạt động của LangGraph, đo lường độ trễ (latency), lượng token tiêu thụ, và lưu log chi tiết từng bước (Supervisor -> Sub-agents -> LLM).

## Tasks
- [x] Tạo `langfuse_service.py` chứa client hoặc callback handler.
- [x] Tích hợp `LangfuseCallbackHandler` vào LangGraph execution (`chat.py` hoặc `builder.py`).
- [x] Áp dụng decorator hoặc truyền callback để trace các API gọi LLM, Qdrant search.
- [x] Update `system_status` API để bao gồm trạng thái của LangFuse.

## Test Criteria
- [ ] Khi chat, LangFuse có log lại các Trace và Span tương ứng với các Node (supervisor, wiki_agent, etc.).
- [ ] Không làm crash ứng dụng nếu LangFuse server (local) bị down.
