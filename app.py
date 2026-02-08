from flask import Flask, render_template, request, redirect, url_for
import json
import os

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
            return json.loads(content)
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
        if task:
            todos.append({"task": task, "done": False})
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