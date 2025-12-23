# Create and return a configured SQLite database connection
import sqlite3

def connect(db_path: str) -> sqlite3.Connection:
    # Always create a NEW connection (no globals, no caching)
    conn = sqlite3.connect(
        db_path,
        check_same_thread=False,  
        timeout=30
    )
    conn.row_factory = sqlite3.Row
    return conn


"""
check_same_thread=False : allows SQLite connections to work in multi-threaded FastAPI environments.
TO AVOID THE ERROR: SQLite objects created in a thread can only be used in that same thread
So:
Request-1 → Connection-A (Thread-1)
Request-2 → Connection-B (Thread-2)
No crash

timeout=30 : SQLite allows many readers, but writes lock the database.
Example:
Request A starts writing (INSERT/UPDATE) → SQLite places a write lock
Request B (new connection) also tries to write or sometimes read also
Request B cannot proceed immediately because the DB is locked
Without a timeout, SQLite will quickly fail with: sqlite3.OperationalError: database is locked
with timeout, If the database is locked, wait up to 30 seconds for the lock to be released before throwing an error.

without row factory: row = (1, "no alcohol")
with row factory:  A dict-like object
row = {
  "habit_id": 1,
  "name": "no alcohol"
}
"""