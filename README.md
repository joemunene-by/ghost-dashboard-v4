# 👻 Ghost Dashboard v4.0

A premium developer dashboard with terminal aesthetics, AI-powered insights, and real-time monitoring.

## Features
- 📊 GitHub repo analytics (public + private)
- 🟩 Contribution heatmap
- 👻 Ghost AI chat (Groq powered)
- ✍️ AI commit message generator
- 🔍 AI code reviewer
- 🐳 Docker container monitoring
- 💻 System metrics
- 🔒 Repo ignore list

## Stack
- **Frontend:** Next.js 16 + Tailwind
- **Backend:** FastAPI + Python
- **AI:** Groq (llama-3.1-8b-instant)
- **DB:** PostgreSQL + Redis

## Setup
```bash
# Backend
cd backend && python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your keys
uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```
