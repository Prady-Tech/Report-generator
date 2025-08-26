import sqlite3
import bcrypt

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def add_user(username, password, role="user"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed, role))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User '{username}' already exists.")
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role = result
        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            return True, role
    return False, None
