# BRIEF: WIKI-AI (Tiếng Việt)

## 1. Mục tiêu dự án
Xây dựng trợ lý AI chạy cục bộ (local-first) để tra cứu tri thức WIKI nội bộ và hỗ trợ hội thoại.  
Hệ thống phải vận hành ổn định trên cấu hình giới hạn (Intel i3-12100, UHD 730, RAM 16GB), ưu tiên tốc độ truy vấn và độ đúng của kết quả.

## 2. Kết quả cốt lõi
- Cung cấp tìm kiếm tri thức WIKI chất lượng cao, có trích nguồn rõ ràng.
- Hỗ trợ hội thoại nhiều lượt với lịch sử phiên chat và ngữ cảnh cơ bản theo người dùng.
- Tối ưu suy luận và truy xuất phù hợp môi trường chạy cục bộ.
- Duy trì trải nghiệm giao diện đơn giản, tập trung vào năng suất chat.

## 3. Phạm vi (giai đoạn hiện tại)
- Giao diện chat có sidebar, danh sách phiên, tạo chat mới và chuyển đổi giao diện sáng/tối.
- API backend cho gửi chat, liệt kê phiên và lấy tin nhắn theo phiên.
- Lưu trữ lai (hybrid storage):
  - Qdrant cho tìm kiếm vector.
  - SQLite cho dữ liệu quan hệ/phiên.
  - Redis hoặc JSON cục bộ cho bộ nhớ hồ sơ nhẹ.
- Điều phối bằng LangGraph với Supervisor và các sub-agent chuyên biệt.

## 4. Yêu cầu chức năng
- Người dùng gửi tin nhắn và nhận phản hồi trợ lý trong cùng phiên.
- Người dùng tạo/chọn/đổi tên/xóa/khôi phục phiên chat.
- Hệ thống trả lời dựa trên WIKI khi độ tin cậy truy xuất đạt ngưỡng.
- Hệ thống fallback an toàn khi chất lượng truy xuất thấp.
- Hệ thống cung cấp endpoint health và trạng thái dịch vụ.

## 5. Yêu cầu phi chức năng
- Vận hành local-first, hạn chế phụ thuộc dịch vụ bên ngoài.
- Luồng phản hồi ổn định trong điều kiện phần cứng giới hạn.
- Xử lý lỗi rõ ràng khi backend không khả dụng.
- Giao diện hoạt động tốt trên desktop và mobile.

## 6. Tóm tắt dữ liệu và kiến trúc
- Truy xuất: Qdrant với HNSW và tối ưu lưu trữ on-disk.
- Embedding: `nomic-embed-text-v1.5` (768 chiều).
- Dữ liệu ứng dụng: SQLite gồm `users`, `sessions`, `messages`.
- Điều phối: Supervisor -> agent theo nhánh (wiki/sales/summary/respond).
- Bộ nhớ hồ sơ: Redis hoặc JSON cục bộ.

## 7. Tiêu chí chấp nhận
- Truy vấn WIKI trả về kết quả liên quan trong ngưỡng hiệu năng local.
- Vòng đời phiên chạy đầy đủ: tạo, đọc, đổi tên, xóa mềm, khôi phục.
- Lịch sử chat được lưu và nạp lại đúng.
- Endpoint health backend trả trạng thái dịch vụ nhất quán.
- Khi không có đáp án chính xác, hệ thống trả phản hồi liên quan theo hướng an toàn.

## 8. Test case tối thiểu
- `TC-01` Tìm kiếm tri thức:
  Với dữ liệu WIKI có chủ đề mục tiêu, khi người dùng truy vấn biến thể/từ đồng nghĩa, thì trả kết quả đúng.
- `TC-02` Lưu phiên:
  Với người dùng tạo và đổi tên nhiều chat, khi tải lại ứng dụng, thì phiên và tiêu đề còn đầy đủ.
- `TC-03` Xóa/khôi phục:
  Với một phiên bị xóa, khi mở thư mục chat đã xóa, thì thấy phiên và có thể khôi phục.
- `TC-04` Sẵn sàng backend:
  Với backend đang chạy, khi gửi yêu cầu chat, thì API trả thành công và có phản hồi trợ lý.

## 9. Ngoài phạm vi (brief này)
- Phân quyền nâng cao theo vai trò.
- Gia cố bảo mật auth ở mức production.
- Triển khai cloud đa tenant.

## 10. Ghi chú bàn giao
Tài liệu này được xây dựng dựa trên `docs/DESIGN.md` và dùng làm brief triển khai cho các tác vụ hiện tại.
