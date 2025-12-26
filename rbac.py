import sqlite3

DB_PATH = "scam.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_container_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS container_access (
        container_name TEXT PRIMARY KEY,
        owner_username TEXT NOT NULL,
        assigned_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        container_name TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT,
        exit_code INTEGER
    );
    """)

    conn.commit()
    conn.close()


def get_container_owner(container_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT owner_username
    FROM container_access
    WHERE container_name = ?
    """, (container_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None


def assign_container(container_name: str, username: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO container_access (container_name, owner_username, assigned_at)
    VALUES (?, ?, datetime('now'))
    """, (container_name, username))

    conn.commit()
    conn.close()


def authorize_user(user: dict, container_name: str):
    init_container_table()

    role = user["role"]
    username = user["username"]

    owner = get_container_owner(container_name)

    if role == "admin":
        if owner is None:
            print(f"[INFO] Container '{container_name}' is unassigned.")
            choice = input("Do you want to assign it to a user? (y/n): ").lower()
            if choice == "y":
                target_user = input("Assign to username: ").strip()
                assign_container(container_name, target_user)
                print(f"[INFO] Container '{container_name}' assigned to '{target_user}'")
        return True

    if owner is None:
        print("[ERROR] Container is unassigned. Contact admin.")
        exit(1)

    if owner != username:
        print("[ERROR] Access denied. You do not own this container.")
        exit(1)

    return True