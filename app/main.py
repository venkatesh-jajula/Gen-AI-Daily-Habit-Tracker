from fastapi import FastAPI # FastAPI is modern, High Performance Python Web Framework used to build APIs quickly and efficiently.
# It helps us to create REST APIs in Python
# It is very fast (built on Starlette:engine + Pydantic:data validator)
# It has automatic validation (incoming request data) and auto-generated API docs (Swagger UI)
from pydantic import BaseModel
# BaseModel is used to define the structure of data and automatically validate it.
import sqlite3

from app.config import DB_PATH, OPENAI_MODEL, OPENAI_API_KEY
from app.db.sqlite import connect
from app.db.schema import init_schema
from app.agent.graph import build_graph, run_agent

# imports the FastAPI class, which you use to create your web application:
app = FastAPI(title="Daily Habit Tracker")

# --- DB connection (SQLite) ---
def get_conn() -> sqlite3.Connection:
    conn = connect(DB_PATH)
    init_schema(conn)
    return conn

# --- Agent graph (LangGraph) ---
# This code builds the LangGraph agent once and reuses it for all incoming API requests.
_graph = None # module-level cache.

def get_graph():
    global _graph
    if _graph is None:
        #core caching logic : First request → _graph is None → build it OR Later requests → _graph already exists → reuse it
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing. Put it in .env")
        _graph = build_graph(OPENAI_MODEL) #_graph is now a compiled LangGraph agent
    return _graph 


class Msg(BaseModel):
    text: str

@app.post("/message")
def message(payload: Msg):
    graph = get_graph() # get cached agent
    reply = run_agent(graph, payload.text) # creates fresh state, runs the graph, returns final reply
    return {"reply": reply}


"""
module-level cache.
Before startup → _graph is empty
After first request → _graph holds the compiled LangGraph
"""