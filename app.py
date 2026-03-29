from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

TESTING_TODOS = None
app = Flask(__name__)
DATA_FILE = "todos.json"


# -------------------------------
# Load Todos
# -------------------------------
def load_todos():
    if app.config.get("TESTING") and TESTING_TODOS is not None:
        return TESTING_TODOS

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []


# -------------------------------
# Save Todos
# -------------------------------
def save_todos(todos):
    if app.config.get("TESTING") and TESTING_TODOS is not None:
        return
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


# -------------------------------
# HOME PAGE
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    todos = load_todos()

    # ----------------
    # ADD TASK
    # ----------------
    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")

        if task:
            todos.append({
                "task": task,
                "description": description,
                "priority": priority,
                "due_date": due_date,
                "done": False,
                "created_at": datetime.now().isoformat()
            })
            save_todos(todos)
        return redirect(url_for("index"))

    # ----------------
    # SEARCH
    # ----------------
    q = request.args.get("q")
    if q:
        todos = [
            t for t in todos
            if q.lower() in t["task"].lower()
            or q.lower() in t.get("description", "").lower()
        ]

    # ----------------
    # FILTER
    # ----------------
    status = request.args.get("status")
    priority_filter = request.args.get("priority")

    if status == "done":
        todos = [t for t in todos if t["done"]]
    if status == "todo":
        todos = [t for t in todos if not t["done"]]
    if priority_filter:
        todos = [t for t in todos if t.get("priority") == priority_filter]

    # ----------------
    # SORT
    # ----------------
    sort = request.args.get("sort")
    if sort == "due":
        todos.sort(key=lambda x: x.get("due_date") or "")
    if sort == "created":
        todos.sort(key=lambda x: x.get("created_at") or "")

    # ----------------
    # STATS
    # ----------------
    total = len(todos)
    completed = sum(1 for t in todos if t["done"])

    return render_template(
        "index.html",
        todos=todos,
        total=total,
        completed=completed
    )


# -------------------------------
# TOGGLE DONE
# -------------------------------
@app.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
        save_todos(todos)
    return redirect(url_for("index"))


# -------------------------------
# DELETE
# -------------------------------
@app.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for("index"))


# -------------------------------
# RUN APP
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
