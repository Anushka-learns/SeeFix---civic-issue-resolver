import sqlite3

DB_NAME = "seefix.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Reports table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        prediction TEXT,
        address TEXT,
        urgency TEXT,
        severity_score REAL,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # Default Admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )

    # Default User
    cursor.execute("SELECT * FROM users WHERE username='user'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("user", "user123", "user")
        )

    conn.commit()
    conn.close()


def save_report(prediction, urgency, severity_score, image_path, address="Unknown"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (image, prediction, address, urgency, severity_score)
        VALUES (?, ?, ?, ?, ?)
    """, (image_path, prediction, address, urgency, severity_score))

    complaint_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return complaint_id


def get_reports():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports ORDER BY severity_score DESC")
    reports = cursor.fetchall()

    conn.close()
    return reports