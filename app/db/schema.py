import sqlite3

def init_schema(conn):
    cur = conn.cursor()

    # Table 1: habits (master list)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1 
                )
""")
    
    # Table 2: habit_ticks (tick events)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habit_ticks(
                tick_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                tick_date TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(habit_id, tick_date),
                FOREIGN KEY(habit_id) REFERENCES habits(habit_id)
                )
""")
    conn.commit()

"""
IN table:2 - UNIQUE(habit_id, tick_date) : Can tick the same habit only once per day.

In table:1 - is_active column is a status flag used in your database to indicate whether a habit is currently enabled or disabled.
is_active = 1 → Active habit
is_active = 0 → Inactive (soft-deleted) habit
"""