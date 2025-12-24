import sqlite3
import hashlib
import os
import getpass
import time

DB_PATH = "scam.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    """)

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(username: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists


def has_any_user() -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    conn.close()
    return count > 0


def create_user(username: str, password: str, role: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (username, password_hash, role, created_at)
    VALUES (?, ?, ?, datetime('now'))
    """, (username, hash_password(password), role))

    conn.commit()
    conn.close()


def authenticate_user():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, password_hash, role
    FROM users
    WHERE username = ?
    """, (username,))

    row = cursor.fetchone()

    if row is None:
        print("[ERROR] Authentication failed")
        time.sleep(1)
        exit(1)

    stored_hash = row[1]
    if stored_hash != hash_password(password):
        print("[ERROR] Authentication failed")
        time.sleep(1)
        exit(1)

    cursor.execute("""
    UPDATE users
    SET last_login = datetime('now')
    WHERE username = ?
    """, (username,))
    conn.commit()

    conn.close()

    print(f"[INFO] Authenticated as '{username}' ({row[2]})")

    return {
        "username": row[0],
        "role": row[2]
    }


def bootstrap_first_user():
    if has_any_user():
        return

    print("[SETUP] No users found. Creating initial admin user.")

    while True:
        username = input("Admin username: ").strip()
        if username:
            break
        print("Username cannot be empty")

    while True:
        password = getpass.getpass("Admin password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password == confirm and password:
            break
        print("Passwords do not match or empty")

    create_user(username, password, role="admin")
    print(f"[SETUP] Admin user '{username}' created successfully\n")
