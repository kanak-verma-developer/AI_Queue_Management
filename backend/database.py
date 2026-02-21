import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "queue.db")


# Fix: Added 2 blank lines above (E302)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token INTEGER,
            name TEXT,
            priority TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def insert_person(token, name, priority):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO queue (token, name, priority) VALUES (?, ?, ?)",
        (token, name, priority)
    )

    conn.commit()
    conn.close()


def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT token, name, priority FROM queue ORDER BY id")
    data = c.fetchall()

    conn.close()
    return data


def clear_queue():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM queue")

    conn.commit()
    conn.close()