# 🎨 DESIGN: WIKI-AI

**Ngày tạo:** 2026-03-05
**Kiến trúc sư:** Minh (Antigravity Architect)
**Dựa trên:** [BRIEF.md](file:///D:/Google%20Antigravity/WIKI-AI/docs/BRIEF.md)

---

## 1. Cách Lưu Thông Tin (Database)

Hệ thống sử dụng kiến trúc Hybrid Storage để tối ưu hóa giữa tốc độ truy vấn và dung lượng RAM (giới hạn 16GB).

### 📦 Vector Database: Qdrant
- **Algorithm:** HNSW (Hierarchical Navigable Small World).
- **Optimization:** `on_disk: true` (Memmap storage).
- **Embedding Model:** `nomic-embed-text-v1.5` (768 dimensions).
- **Mục đích:** Tìm kiếm ngữ nghĩa kiến thức WIKI.

### 👤 Relational & Session Data: SQLite
- **Bảng `users`:** `id`, `username`, `password_hash`, `avatar_url`.
- **Bảng `sessions`:** `id`, `user_id`, `title`, `created_at`.
- **Bảng `messages`:** `id`, `session_id`, `role` (user/assistant/tool), `content`, `timestamp`.

### 🧠 Profile Memory: Redis (hoặc local JSON)
- **Keys:** `user_profile:{user_id}`, `context_summary:{session_id}`.
- **Mục đích:** Lưu trữ sở thích khách hàng và tóm tắt hội thoại luỹ tiến.

---

## 2. Thiết Kế Luồng Graph (LangGraph)

Hệ thống được tổ chức theo đồ thị có hướng, Supervisor đóng vai trò điều phối.

### 🛰️ Supervisor Node
- **Input:** `User Query`, `Chat History`.
- **Logic:** Sử dụng CoT để quyết định rẽ nhánh:
  - Nếu query về tra cứu -> `wiki_agent`.
  - Nếu query về tài khoản -> `auth_agent`.
  - Nếu query chung -> Trả lời trực tiếp.

### 📚 Wiki Agent Node (Advanced RAG)
1. **Query Expansion:** Mở rộng từ khóa thông qua dictionary.
2. **Search:** Gọi Qdrant API.
3. **Reranking:** Tính toán `rerank_score` dựa trên khớp từ khóa và metadata.
4. **Conclusion:** Nếu `score > threshold` -> Trả về kết quả; nếu không -> Gọi lại bước 1 với query tối giản (CRAG).

---

## 3. Quy Tắc Kiểm Tra (Acceptance Criteria)

### ✅ Tính năng: Tra cứu thông tin (Wiki Search)
- [ ] Truy vấn Qdrant hoàn thành dưới 500ms (Local SSD).
- [ ] Agent nhận diện đúng tên sản phẩm đặc thù nhờ Layer 1 (Synonym Dictionary).
- [ ] Nếu không tìm thấy, hệ thống hiển thị thông báo "Xin lỗi, tôi không tìm thấy thông tin cụ thể nhưng có thông tin liên quan sau..." thay vì trả lời sai.

### ✅ Tính năng: Quản lý tài khoản
- [ ] Đăng nhập/Đăng xuất dưới 200ms.
- [ ] Khi Switch Account, Agent phải ngay lập tức nhận ra context của User mới (Avatar, Lịch sử).

---

## 4. Test Cases

| ID | Case | Given | When | Then |
|----|------|-------|------|------|
| TC-01 | Wiki Search | Wiki có doc "Sữa hạt Macca" | Tìm "hạt macca" | Trả về thông tin Sữa hạt Macca |
| TC-02 | Memory Persistence | User thích màu xanh | Sau 5 câu hỏi hỏi "Tôi thích màu gì?" | Agent trả lời "Xanh" |
| TC-03 | SYCL Validation | LLM đang inference | Monitor taskmanager | GPU UHD 730 có mức sử dụng > 50% |

---
*Tạo bởi AWF 2.1 - Design Phase*
