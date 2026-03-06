# Phase 01: Project Setup & Foundation

## Objective
Thiết lập môi trường phát triển cơ bản, cấu trúc thư mục và khởi chạy các server (Backend/Frontend).

## Tasks
- [x] Khởi tạo dự án Vite + React + TailwindCSS cho Frontend.
- [x] Cấu hình Python venv và cài đặt core dependencies (FastAPI, LangGraph, LangFuse, IPEX-LLM).
- [x] Thiết lập thư mục `data/` cho Vector DB và `assets/` cho WIKI data.
- [x] Tạo file `.env` với các tham số mẫu.

## Files to Create
- `backend/main.py`: Entry point cho FastAPI.
- `frontend/`: Toàn bộ source code giao diện.
- `docker-compose.yml`: (Optional) Cho self-hosted LangFuse & Redis.

## Test Criteria
- [ ] Backend chạy tại `localhost:8000/docs`.
- [ ] Frontend chạy tại `localhost:5173`.
