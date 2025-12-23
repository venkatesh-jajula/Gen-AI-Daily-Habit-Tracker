import sqlite3
from datetime import date, timedelta
from typing import Any, Dict, List, Tuple

def _monday_sunday_range(ref: date) -> Tuple[date, date]: # If ref = 2025-12-25 (Thursday)
    """Given any date, this function returns: the Monday of that week & the Sunday of that week"""
    monday = ref - timedelta(days=ref.weekday())  # → 3
    sunday = monday + timedelta(days=6) # Monday, add 6 days → Sunday.
    return monday, sunday

def weekly_summary_calendar_week(conn: sqlite3.Connection, ref_date: date | None = None) -> Dict[str, Any]:
    """weekly habit summary for the calendar week (Mon - Sun)."""
    ref_date = ref_date or date.today()
    week_start, week_end = _monday_sunday_range(ref_date) # Monday, Sunday
    cur = conn.cursor()
    cur.execute("SELECT habit_id, name FROM habits WHERE is_active=1 ORDER BY lower(name)") #Fetches all habits only active ones
    habits = cur.fetchall()
    results: List[Dict[str, Any]] = []
    for h in habits: #Loop through each habits (master habits) : calculate stats habit by habit.
        cur.execute("""
            SELECT tick_date FROM habit_ticks
            WHERE habit_id=? AND tick_date BETWEEN ? AND ?
        """, (h["habit_id"], week_start.isoformat(), week_end.isoformat())) #Fetches only the days when the habit was ticked Between Monday and Sunday.
        tick_dates = {r["tick_date"] for r in cur.fetchall()} # Creates a set of dates where habit was completed.
        ticked_days = len(tick_dates) # Counts how many days the habit was done that week.
        # Building summary stats per habit
        results.append({ 
            "habit": h["name"],
            "ticked_days": ticked_days,
            "missed_days": 7 - ticked_days,
            "adherence_pct": round((ticked_days / 7) * 100, 1),
        })
    # Final return value
    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "habits": results
    }