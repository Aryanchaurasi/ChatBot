# DualLLM TruthBot

A production-ready full-stack multi-LLM chatbot that queries Gemini 1.5 Flash + GPT-4o-mini simultaneously, compares responses using a judge LLM, and shows users the "most accurate" answer with reasoning.

## 🚀 Features

- ✅ **Dual LLM Comparison**: Gemini 1.5 Flash vs GPT-4o-mini
- ✅ **AI Judge**: GPT-4o-mini evaluates which response is better
- ✅ **Split-screen UI**: Best answer + comparison view
- ✅ **Confidence Scores**: 0-100% confidence ratings
- ✅ **Chat History**: SQLite database storage
- ✅ **Real-time Responses**: Parallel API calls for speed
- ✅ **Copy/Share**: Easy response sharing
- ✅ **Error Handling**: Graceful API failure handling
- ✅ **Docker Ready**: Full containerization

## 🛠 Tech Stack

**Backend**: FastAPI + LiteLLM + Uvicorn + Python 3.11  
**Frontend**: React 18 + Vite + TypeScript + Tailwind CSS  
**Database**: SQLite (chat history)  
**Deployment**: Docker Compose ready

## 📦 Quick Start

### 1. Clone and Setup Environment

```bash
git clone <repo-url>
cd ChatBot

# Copy environment file
cp backend/.env.example backend/.env
```

### 2. Add API Keys

Edit `backend/.env`:
```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
DATABASE_URL=sqlite:///./truthbot.db
ORIGINS=http://localhost:3000
```

### 3. Run with Docker Compose

```bash
docker compose up --build
```

Visit: http://localhost:3000

### 4. Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🎯 How It Works

1. **User Query** → Frontend sends to `/api/chat`
2. **Parallel LLM Calls** → FastAPI queries both Gemini & OpenAI simultaneously
3. **Judge Evaluation** → GPT-4o-mini compares responses and picks winner
4. **Response Display** → UI shows best answer + comparison + reasoning
5. **Database Storage** → Chat history saved with timestamps

## 📁 Project Structure

```
ChatBot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── database.py          # DB connection
│   │   ├── services/
│   │   │   └── llm_service.py   # LLM logic + judge
│   │   └── routers/
│   │       └── chat.py          # Chat endpoints
│   ├── requirements.txt
│   ├── .env
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx   # Main chat interface
│   │   │   ├── MessageBubble.tsx # Message display
│   │   │   └── ChatInput.tsx    # Input component
│   │   ├── hooks/
│   │   │   └── useChat.ts       # Chat logic hook
│   │   └── lib/
│   │       └── utils.ts         # API utilities
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```

## 🎨 UI Preview

```
┌─ DualLLM TruthBot ──────────────────────────────┐
│ Query: "Best Python framework 2025?"           │
├─ 🏆 BEST (95% conf) ──────────────────────────┤
│ FastAPI - Judge: "Most complete reasoning"     │
├─ COMPARISON ──────────────────────────────────┤
│ 🦒 Gemini: "Django..." | 🔥 OpenAI: "FastAPI" │
│ ⚖️ Judge: "OpenAI more current + benchmarks"   │
└─ [Type your message...] [Send] ────────────────┘
```

## 🔧 API Endpoints

- `POST /api/chat` - Send chat message
- `GET /api/history/{session_id}` - Get chat history
- `GET /` - API status
- `GET /health` - Health check
- `GET /docs` - FastAPI documentation

## 🚀 Production Deployment

### Vercel (Frontend)
```bash
cd frontend
npm run build
# Deploy dist/ folder to Vercel
```

### Render (Backend)
```bash
# Push to GitHub
# Connect Render to repo
# Set environment variables in Render dashboard
```

### Environment Variables for Production
```env
OPENAI_API_KEY=sk-proj-...
GEMINI_API_KEY=AIzaSy...
DATABASE_URL=sqlite:///./truthbot.db
ORIGINS=https://your-frontend-domain.com
```

## 🔍 Judge Logic

The judge uses this prompt structure:
```
Query: {user_question}
Response A (Gemini): {gemini_response}
Response B (OpenAI): {openai_response}

Pick BEST (A/B/tie). Explain why in 1 sentence.
Return JSON: {"winner": "A", "reason": "explanation", "confidence": 0.95}
```

## 🛡 Error Handling

- API key validation
- Rate limiting (10 req/min)
- Graceful LLM API failures
- Database connection errors
- Network timeout handling

## 📊 Performance

- **Parallel API calls** reduce response time by ~50%
- **SQLite** for fast local storage
- **React 18** with optimized re-renders
- **Vite** for fast development builds

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ using FastAPI + React + LiteLLM**