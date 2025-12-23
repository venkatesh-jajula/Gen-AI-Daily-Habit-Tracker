import sqlite3
from datetime import datetime, timezone

class HabitRepository:
    def __init__(self, conn):
        self.conn = conn
    
    def add_habit(self, name):
        name = name.strip()
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO habits (name, created_at, is_active) VALUES (?, ?, 1)",
            (name,datetime.now(timezone.utc).isoformat()))
            self.conn.commit()
            return f"Added Habit: {name}"
        except sqlite3.IntegrityError:
            return f"Habit already exists: {name}"
        
    def get_habit_id(self,name):
        cur = self.conn.cursor()
        cur.execute("SELECT habit_id FROM habits WHERE lower(name)=lower(?) AND is_active=1", (name.strip(),)) # why , at last : SQLite expects a tuple for parameters not just a string
        row = cur.fetchone()
        return int(row["habit_id"]) if row else None
    
    def tick_habit(self,name,tick_dt):
        habit_id = self.get_habit_id(name)
        if habit_id is None:
            return f"Habit not found: {name}. Add it first"
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO habit_ticks (habit_id,tick_date,created_at) VALUES (?,?,?)", (habit_id,tick_dt.isoformat(),datetime.now(timezone.utc).isoformat()))
            self.conn.commit()
            return f"Ticked {name} for {tick_dt.isoformat()}."
        except sqlite3.IntegrityError:
            return f"Already Ticked '{name}' for {tick_dt.isoformat()}."
    

"""Database Operations"""            