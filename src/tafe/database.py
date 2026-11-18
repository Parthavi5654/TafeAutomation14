
import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/reminder_history.db")


def get_connection():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS reminder_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                mobile TEXT NOT NULL,
                pending_amount REAL NOT NULL,
                sent_at TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_customer_reminders
            ON reminder_history(customer_id, sent_at)
        """)


def get_last_successful_reminder(customer_id):

    with get_connection() as connection:

        result = connection.execute("""
            SELECT sent_at
            FROM reminder_history
            WHERE customer_id = ?
              AND status = 'accepted'
            ORDER BY sent_at DESC
            LIMIT 1
        """, (customer_id,)).fetchone()

    if result:
        return datetime.fromisoformat(result["sent_at"])

    return None


def record_reminder(customer_id, mobile, pending_amount, status):

    with get_connection() as connection:

        connection.execute("""
            INSERT INTO reminder_history (
                customer_id,
                mobile,
                pending_amount,
                sent_at,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            mobile,
            pending_amount,
            datetime.now().astimezone().isoformat(),
            status
        ))
