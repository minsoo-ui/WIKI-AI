# 🧠 WIKI-AI

> Local AI Agent for WIKI-Database, optimized for Intel i3-12100 & UHD 730 (SYCL).

## 🚀 Quick Start

### 1. Backend (Python)
```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

### 3. Services (Docker)
```bash
docker compose up -d    # Qdrant + Redis + LangFuse
```

## 📁 Project Structure
```
WIKI-AI/
├── backend/             # Python FastAPI + LangGraph
│   ├── app/
│   │   ├── api/         # REST endpoints (chat, auth)
│   │   ├── config.py    # Centralized settings
│   │   └── main.py      # FastAPI entry point
│   └── requirements.txt
├── frontend/            # React + Vite + TailwindCSS
│   ├── src/
│   │   ├── components/  # UI components (Sidebar, ChatArea)
│   │   ├── App.jsx      # Main layout
│   │   └── index.css    # Design system (Light/Dark)
│   └── package.json
├── data/                # SQLite + Qdrant storage
├── assets/              # Raw WIKI data files
├── docs/                # BRIEF, DESIGN, Specs
├── .env                 # Environment configuration
└── docker-compose.yml   # Qdrant, Redis, LangFuse
```

## 🏗️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 19 + Vite 6 + TailwindCSS 4 |
| Backend | Python + FastAPI + LangGraph |
| Vector DB | Qdrant (memmap storage) |
| Database | SQLite |
| AI Engine | IPEX-LLM (SYCL) |
| Observability | LangFuse (self-hosted) |

## 📄 License
Private - Internal Use Only
