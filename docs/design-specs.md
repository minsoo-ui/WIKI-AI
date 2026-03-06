/# Design Specifications: WIKI-AI

## 🎨 Vibe & Style
- **Phong cách:** Minimalist (Tối giản), Friendly (Thân thiện).
- **Trải nghiệm:** Tập trung vào nội dung chat, giảm thiểu sự phân tâm.

## 🌗 Theme System
- **Theme Toggle:** Nút chuyển đổi giao diện đặt tại **góc trên cùng bên phải** của màn hình chính (Header/Top-right corner).
- **Light Mode:**
  - Background: `#F9FAFB`
  - Surface: `#FFFFFF`
  - Text: `#111827`
  - Border: `#E5E7EB`
- **Dark Mode:**
  - Background: `#0F172A`
  - Surface: `#1E293B`
  - Text: `#F1F5F9`
  - Border: `#334155`

## 📐 Layout & Structure
- **Sidebar (Left):** Rộng 260px.
  - **Top (User Space):** 
    - **User Profile Card:** Hiển thị Avatar, Tên người dùng và Email.
    - **Account Actions:** Nút 'Switch Account' và 'Logout' đặt ngay dưới thông tin User.
  - **Middle:** Nút 'New Chat' và danh sách lịch sử phiên chat.
  - **Bottom:** Các danh mục WIKI/Database hoặc thông số hệ thống.
- **Main Chat Area (Center):** Max-width 800px. Header chứa nút Theme Toggle ở góc phải.

## 📝 Typography
- **Font:** Inter (Google Fonts).
- **Body:** 16px, Line-height 1.6.
- **Header:** Semi-bold, tăng kích thước phân cấp rõ ràng.

## ✨ Micro-interactions
- **Hover effects:** Hiệu ứng làm sáng nhẹ hoặc đổi màu biên khi di chuột qua các mục lục ở Sidebar.
- **Transitions:** Chuyển đổi mượt mà (300ms) giữa Light và Dark mode.
