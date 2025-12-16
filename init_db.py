import sqlite3

db = sqlite3.connect("todo.db")

db.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

db.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    priority INTEGER,
    due_date TEXT,
    done INTEGER DEFAULT 0
)
""")

db.commit()
db.close()

print("Database created successfully ✅")
