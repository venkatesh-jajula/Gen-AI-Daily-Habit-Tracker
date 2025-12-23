from langchain.tools import tool
from datetime import date
import dateparser
import sqlite3

from app.db.repo import HabitRepository
from app.services.summary_service import weekly_summary_calendar_week

def _parse_date(day: str | None) -> date:
    """Helper function: converts whatever the user types (like 'today','yesterday','last Monday' or '2025-12-21') into a proper python date object
    Ex: User says:'tick no alchol' ->no day provided ->it ticks today"""
    if not day:
        return date.today()
    # It tries to understand natural language date phrases like: today, yesterday, last monday, 3 days ago, 2025-12-21
    # PREFER_DATES_FROM: "past" means: If a phrase is ambiguous (like “Monday”), it will prefer the previous Monday rather than a future Monday.
    dt = dateparser.parse(day, settings={"PREFER_DATES_FROM":"past"})
    return dt.date() if dt else date.today()

@tool
def add_habit(name):
    """Add a new habit (default state is unticked)"""
    from app.main import get_conn 
    conn: sqlite3.Connection = get_conn() 
    try:
        return HabitRepository(conn).add_habit(name)
    finally:
        conn.close()

@tool
def tick_habit(name:str,day:str|None = None)->str:
    """Tick a habit for the given day (default today)."""
    from app.main import get_conn
    conn: sqlite3.Connection = get_conn() 
    tick_dt = _parse_date(day)
    try:
        return HabitRepository(conn).tick_habit(name,tick_dt)
    finally:
        conn.close()

@tool
def get_weekly_summary(ref_day: str | None = None) -> dict:
    """Calendar-week summary(MON-SUN) for the week containing ref_day(default today)."""
    from app.main import get_conn
    conn: sqlite3.Connection = get_conn()
    ref_dt = _parse_date(ref_day)
    try:
        return weekly_summary_calendar_week(conn, ref_dt)
    finally:
        conn.close()