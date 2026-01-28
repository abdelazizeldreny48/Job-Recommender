import sqlite3
import hashlib

# ------------------ DB Setup ------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        skills TEXT
    )
    """)

    conn.commit()
    conn.close()

# ------------------ Hash Password ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ Register ------------------
def register_user(full_name, email, password):
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users(full_name, email, password) VALUES (?,?,?)",
                       (full_name, email, hash_password(password)))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        return False

# ------------------ Login ------------------
def login_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, full_name FROM users WHERE email=? AND password=?",
                   (email, hash_password(password)))

    result = cursor.fetchone()
    conn.close()

    return result  # (id, name) OR None

# ------------------ Save skills ------------------
def save_user_skills(user_id, skills):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET skills=? WHERE id=?", (skills, user_id))
    conn.commit()
    conn.close()

# ------------------ Load skills ------------------
def load_user_skills(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT skills FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    return row[0] if row else ""
