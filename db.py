import sqlite3

DATABASE_PATH = "neon.db"

def init_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        # Example: Create a users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            profile_pic TEXT
        )
        """)
        conn.commit()

def init_db_command():
    """Command to initialize the database."""
    init_db()
    print("Database initialized.")
