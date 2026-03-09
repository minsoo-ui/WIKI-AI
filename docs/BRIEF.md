# BRIEF: WIKI-AI

## 1. Project Goal
Build a local-first AI assistant for internal WIKI knowledge lookup and chat support.  
The system must run reliably on a constrained machine profile (Intel i3-12100, UHD 730, 16GB RAM) and prioritize fast, correct retrieval over broad feature scope.

## 2. Core Outcomes
- Provide high-quality WIKI knowledge search with traceable source snippets.
- Support multi-turn chat with session history and basic account context.
- Keep inference and retrieval practical for local deployment.
- Maintain a simple UX focused on chat productivity.

## 3. Scope (Current Phase)
- Chat interface with sidebar, session list, new chat flow, and theme toggle.
- Backend API for chat sending, session listing, and message retrieval.
- Hybrid storage:
  - Qdrant for vector search.
  - SQLite for relational/session data.
  - Redis or local JSON for lightweight memory profile.
- LangGraph orchestration with Supervisor routing and specialized sub-agents.

## 4. Functional Requirements
- User can send a message and receive an assistant reply in the same session.
- User can create/select/rename/delete/restore chat sessions.
- System returns WIKI-based answers when retrieval confidence is acceptable.
- System falls back safely when retrieval quality is low.
- System exposes health and service status endpoints.

## 5. Non-Functional Requirements
- Local-first operation with minimal external dependencies.
- Stable response flow under limited hardware resources.
- Clear error handling for backend unavailable states.
- Mobile-friendly and desktop-friendly UI behavior.

## 6. Data and Architecture Summary
- Retrieval: Qdrant with HNSW and on-disk optimization.
- Embeddings: `nomic-embed-text-v1.5` (768 dimensions).
- App data: SQLite tables for `users`, `sessions`, `messages`.
- Orchestration: Supervisor -> routed agent (wiki/sales/summary/respond).
- Memory profile: Redis or local JSON fallback.

## 7. Acceptance Criteria
- WIKI query returns relevant result under local performance target.
- Session lifecycle works end-to-end: create, read, update title, soft delete, restore.
- Chat history persists and reloads correctly.
- Backend health endpoint returns service status consistently.
- When exact answer is unavailable, system returns a safe related-response fallback.

## 8. Test Cases (Minimum)
- `TC-01` Knowledge Search:
  Given WIKI contains target topic, when user queries synonym/variant, then relevant doc is returned.
- `TC-02` Session Persistence:
  Given user creates and renames chats, when app reloads, then sessions and titles remain available.
- `TC-03` Delete/Restore Flow:
  Given a session is deleted, when opening deleted folder, then chat is visible and can be restored.
- `TC-04` Backend Availability:
  Given backend is running, when sending a chat request, then API returns success and assistant response.

## 9. Out of Scope (This Brief)
- Advanced role/permission system.
- Full production auth hardening.
- Cloud multi-tenant deployment.

## 10. Delivery Note
This brief is derived from `docs/DESIGN.md` and is intended as the implementation reference for current development tasks.
