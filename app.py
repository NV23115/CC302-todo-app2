from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime


app = Flask(__name__)
DATA_FILE = "todos.json"


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []

            todos = json.loads(content)

            # Backward compatibility for old todos
            for t in todos:
                t.setdefault("description", "")
                t.setdefault("priority", "medium")
                t.setdefault("due_date", "")
                t.setdefault("status", "todo")
                t.setdefault("created_at", "")

            return todos

    except json.JSONDecodeError:
        return []


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def index():
    todos = load_todos()

    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date")

        if task:
            new_todo = {
                "task": task,
                "description": description,
                "priority": priority,
                "due_date": due_date,
                "status": "todo",
                "created_at": datetime.now().isoformat(),
                "done": False
            }

            todos.append(new_todo)
            save_todos(todos)

        return redirect(url_for("index"))

    total = len(todos)
    completed = sum(1 for t in todos if t["done"])

    return render_template(
        "index.html",
        todos=todos,
        total=total,
        completed=completed
    )


@app.route("/toggle/<int:index>")
def toggle(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
        save_todos(todos)
    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    todos = load_todos()
    new_task = request.form.get("task")

    if new_task and 0 <= index < len(todos):
        todos[index]["task"] = new_task
        save_todos(todos)

    return redirect(url_for("index"))


@app.route("/delete/<int:index>")
def delete(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
