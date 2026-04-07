Here is your complete README.md file. Copy and paste this entire code block directly into your `README.md` file.

---

```markdown
# AI Chatbot API

A production-ready conversational AI chatbot with persistent memory, built with FastAPI and Google's Gemini API.

## Video Demonstration

[Click here for video demonstration - Google Drive](https://drive.google.com/drive/folders/1iJHaBhAP3Z9s3MasBvT8G5GjhM-3ntGr?usp=drive_link)

## Features

- Multi-turn conversation with context memory
- Session isolation (different users don't interfere)
- RESTful API with FastAPI
- Docker containerization
- Thread-safe in-memory storage
- Automatic API documentation (Swagger UI)
- Health checks and error handling
- Session management (create, read, clear, delete)

## Technology Stack

- Framework: FastAPI (Python 3.11)
- AI Model: Google Gemini Pro (Free)
- Memory: In-memory dictionary (thread-safe)
- Container: Docker + Docker Compose

## Prerequisites

- Python 3.11 or higher
- Docker Desktop (optional, for containerized deployment)
- Git
- Google Gemini API key (free)

## Quick Start (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/maksudrakib44/AI-Chatbot
cd AI-Chatbot
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
LLM_MODEL=gemini-1.5-flash
HOST=0.0.0.0
PORT=8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
uvicorn app.main:app --reload
```

### 5. Access the API

Open your browser to: http://localhost:8000/docs

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

### Stop the Container

```bash
docker-compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Send a message to the AI |
| GET | /api/history/{session_id} | Get conversation history |
| DELETE | /api/history/{session_id} | Clear session history |
| DELETE | /api/session/{session_id} | Delete session completely |
| GET | /api/health | Health check |
| GET | /api/sessions | List all active sessions |

## API Usage Examples

### Send a Message

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "message": "Hi, my name is Maksud"
  }'
```

**Response:**
```json
{
  "session_id": "user123",
  "response": "Hello Maksudul! Nice to meet you. How can I help you today?",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### Test Memory (Follow-up Message)

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "message": "What is my name?"
  }'
```

**Response:**
```json
{
  "session_id": "user123",
  "response": "Your name is Maks. You told me that earlier.",
  "timestamp": "2024-01-15T10:30:05.123456"
}
```

### Get Conversation History

```bash
curl http://localhost:8000/api/history/user123
```

**Response:**
```json
{
  "session_id": "user123",
  "history": [
    {"role": "user", "content": "Hi, my name is John"},
    {"role": "assistant", "content": "Hello John! Nice to meet you."},
    {"role": "user", "content": "What is my name?"},
    {"role": "assistant", "content": "Your name is John."}
  ],
  "total_messages": 4
}
```

### Clear Session History

```bash
curl -X DELETE http://localhost:8000/api/history/user123
```

**Response:**
```json
{
  "status": "success",
  "message": "History cleared for session: user123",
  "session_id": "user123"
}
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

## Project Structure

```
ai-chatbot-task/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py          # API route handlers
│   └── services/
│       ├── __init__.py
│       ├── ai.py            # Gemini API integration
│       └── memory.py        # Session memory management
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Architecture Explanation

### Design Decisions

**1. In-Memory Storage**
- Selected for simplicity and speed in this assessment
- Thread-safe implementation using locks for concurrent requests
- Can be easily replaced with Redis or PostgreSQL for production

**2. Session Isolation**
- Each session uses a unique `session_id` as a dictionary key
- Messages are stored per session ensuring complete isolation
- No cross-session data leakage possible

**3. AI Model Integration**
- Google Gemini API chosen for free tier availability
- Full conversation history passed to AI on every request
- System prompt guides consistent AI behavior

**4. Thread Safety**
- `threading.Lock` ensures safe concurrent access
- Prevents race conditions during simultaneous requests

### Data Flow

```
Client Request (POST /api/chat)
         |
         v
FastAPI Route Handler
         |
         v
Memory Service (save user message)
         |
         v
AI Service (get response with full history)
         |
         v
Memory Service (save assistant response)
         |
         v
JSON Response to Client
```

## Testing

### Using Swagger UI (Recommended)

1. Start the server: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Test each endpoint interactively

### Using cURL Commands

```bash
# Health check
curl http://localhost:8000/api/health

# Send first message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"Hi, my name is Maksud"}'

# Send second message (tests memory)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"What is my name?"}'

# Get history
curl http://localhost:8000/api/history/test

# Clear history
curl -X DELETE http://localhost:8000/api/history/test
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | Run `pip install -r requirements.txt` |
| `GEMINI_API_KEY not found` | Create `.env` file with your actual API key |
| `Address already in use` | Change port: `uvicorn app.main:app --port 8001` |
| `Model not found error` | Update `LLM_MODEL=gemini-1.5-flash` in `.env` |
| Docker container won't start | Ensure Docker Desktop is running |
| API returns 500 error | Check terminal for detailed error message |

## Submission Checklist

- All API endpoints work correctly
- Memory persists across multiple turns
- Sessions are strictly isolated
- Docker setup works with one command
- Video demo included in README
- Code is modular and well-documented
- Environment variables properly configured

## Author

Md. Maksudul Haque
