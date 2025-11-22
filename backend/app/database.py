import sqlite3
import os
from datetime import datetime

# Use environment variable for DB path, with fallback
DB_PATH = os.getenv("DB_PATH", "qa_logs.db")

def get_db_connection():
    # Ensure directory exists - FIXED VERSION
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:  # Only create if there's a directory path
        os.makedirs(db_dir, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            language TEXT NOT NULL,
            user_ip TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_qa_interaction(question: str, answer: str, language: str, user_ip: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO qa_logs (question, answer, language, user_ip)
        VALUES (?, ?, ?, ?)
    """, (question, answer, language, user_ip))
    conn.commit()
    conn.close()

def get_recent_logs(limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, question, answer, language, user_ip, timestamp
        FROM qa_logs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    logs = cursor.fetchall()
    conn.close()
    return logs

