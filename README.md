# 🧠 Daily Habit Tracker – GenAI MVP (LangGraph + FastAPI)

A **Generative AI–powered Daily Habit Tracker** built using **LangGraph**, **LangChain**, **FastAPI**, and **SQLite**.  
The system uses an **LLM agent with tool calling** to manage habits, track daily progress, and generate weekly summaries.

---

## 🚀 Features (MVP v1)

- ➕ Add new habits
- ✅ Tick habits for specific days (natural language supported)
- 📊 Generate weekly habit summaries (Monday–Sunday)
- 🤖 LLM-powered agent with deterministic tool usage
- 🧩 Clean separation of concerns (Agent · Tools · DB · Services)
- 🗄️ Persistent storage using SQLite
- 🧠 Stateless API (state per request, DB as memory)
- 📈 Auto-generated LangGraph workflow diagram

---

## 🏗️ Architecture Overview

```
FastAPI
  └── LangGraph Agent
        ├── LLM Node (ChatOpenAI)
        ├── Tools Node (DB-backed tools)
        └── Router (decides tool vs end)
              ↓
           SQLite DB
```

### Agent Design
- **LLM Node**: Reasoning + decision-making
- **Tools Node**: Executes DB-backed actions
- **Router**: Controls agent flow
- **State**: Short-lived per request
- **Database**: Long-term memory

---

## 📂 Project Structure

```
HabitTracker/
│
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── config.py              # Environment config
│   │
│   ├── agent/
│   │   ├── graph.py           # LangGraph workflow
│   │   ├── state.py           # Agent state definition
│   │   └── prompts.py         # System prompt
│   │
│   ├── tools/
│   │   └── habit_tools.py     # Tool definitions
│   │
│   ├── db/
│   │   ├── schema.py          # SQLite schema
│   │   ├── repo.py            # Repository layer
│   │   └── sqlite.py          # DB connection
│   │
│   └── services/
│       └── summary_service.py # Weekly summary logic
│
├── requirements.txt
├── .env                       # Environment variables
├── tracker.db                 # SQLite database (auto-created)
├── workflow.png               # LangGraph workflow diagram
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** – API layer
- **LangGraph** – Agent workflow orchestration
- **LangChain** – Tool calling & messaging
- **OpenAI (ChatOpenAI)** – LLM
- **SQLite** – Persistent storage
- **Mermaid** – Workflow visualization

---

## ⚙️ Setup & Run Instructions

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd HabitTracker
```

### 2️⃣ Create virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env` file

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-5-nano
DB_PATH=tracker.db
```

### 5️⃣ Run the application
```bash
uvicorn app.main:app --reload
```

Server will start at:
```
http://127.0.0.1:8000
```

---

## 🧪 Using the API

### Swagger UI
Open in browser:
```
http://127.0.0.1:8000/docs
```

### Example Requests

**Add a habit**
```json
{ "text": "add habit gym" }
```

**Tick a habit**
```json
{ "text": "tick gym yesterday" }
```

**Weekly summary**
```json
{ "text": "weekly summary" }
```

---

## 📈 Workflow Diagram

our `graph.py` exports the diagram, it will generate:

- `workflow.png`

This image represents the LangGraph execution flow.

---

## 🧠 Key Design Decisions

- **Stateless API**: Each request starts with fresh state
- **Database as memory**: No session memory required
- **Tool-based actions**: LLM cannot mutate data directly
- **Deterministic behavior**: `temperature=0`
- **Clean architecture**: No SQL inside tools or agents

---

## 🧩 Limitations (v1)

- Single-user (no auth / user_id)
- No habit streak analytics
- No session-based memory
- Local SQLite only

---

## 🔮 Future Improvements

- Multi-user support
- Habit streaks & insights
- Authentication & authorization
- Redis / DB-backed session memory
- Dockerization
- Cloud deployment (AWS / Azure)

---

## 🏷️ Versioning

**v1.0.0**
- Initial MVP release
- Core habit tracking functionality
- LangGraph-based agent architecture
---

