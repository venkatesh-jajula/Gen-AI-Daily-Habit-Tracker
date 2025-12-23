import sqlite3
from datetime import datetime, timezone, date

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
    
    def list_active_habits(self)->list[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM habits WHERE is_active=1 ORDER BY lower(name)")
        rows = cur.fetchall()
        return [r["name"] for r in rows]
    
    def daily_status(self,ref_date:date)->list[dict]:
        """It returns the status of all active habits for a given day, showing whether each habit was ticked or not."""
        cur = self.conn.cursor()
        cur.execute("SELECT habit_id, name FROM habits WHERE is_active=1 ORDER BY lower(name)")
        habits = cur.fetchall()
        
        out = []
        for habit in habits:
            cur.execute("SELECT 1 FROM habit_ticks WHERE habit_id=? AND tick_date=? LIMIT 1",
            (habit["habit_id"], ref_date.isoformat()),)
            ticked = cur.fetchone() is not None
            out.append({"habit":habit["name"], "ticked":ticked})
        return out
    

"""Database Operations"""            