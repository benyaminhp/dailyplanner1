from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.secret_key = "cs50_todo_secret"

def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    today = date.today().isoformat()
    db = get_db()
    tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY priority DESC, due_date",
        (session["user_id"],)
    ).fetchall()
    db.close()

    return render_template("index.html", tasks=tasks, today=today)

@app.route("/add", methods=["POST"])
def add():
    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    priority = request.form["priority"]
    due_date = request.form["due_date"]

    db = get_db()
    db.execute(
        "INSERT INTO tasks (user_id, title, priority, due_date) VALUES (?, ?, ?, ?)",
        (session["user_id"], title, priority, due_date)
    )
    db.commit()
    db.close()
    return redirect("/")

@app.route("/done/<int:task_id>")
def done(task_id):
    db = get_db()
    db.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    db.close()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        if db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone():
            error = "Username already exists"
        else:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            db.close()
            return redirect("/login")

    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(port=9000)






