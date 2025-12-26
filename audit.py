import sqlite3
from datetime import datetime

DB_NAME = "scam.db"


def start_session(username: str, container_name: str) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (username, container_name, start_time)
        VALUES (?, ?, ?)
    """, (
        username,
        container_name,
        datetime.utcnow().isoformat()
    ))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return session_id


def end_session(session_id: int, exit_code: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE audit_logs
        SET end_time = ?, exit_code = ?
        WHERE id = ?
    """, (
        datetime.utcnow().isoformat(),
        exit_code,
        session_id
    ))

    conn.commit()
    conn.close()