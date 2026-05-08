import sqlite3
import datetime

DB_NAME = "swiftreply.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        cursor.execute("ALTER TABLE leads ADD COLUMN contact_method TEXT DEFAULT 'Email'")
    except sqlite3.OperationalError:
        pass # Column likely already exists
    conn.commit()
    conn.close()

def save_lead(name: str, email: str, phone: str, contact_method: str = "Email"):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cursor.execute(
        "INSERT INTO leads (name, email, phone, contact_method, timestamp) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone, contact_method, now)
    )
    conn.commit()
    conn.close()

def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
