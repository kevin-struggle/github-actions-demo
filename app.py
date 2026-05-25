from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {"id": 1, "task": "学习 GitHub Actions", "done": False},
    {"id": 2, "task": "完成演示项目", "done": False},
]


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the GitHub Actions Demo API!"})


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "task field is required"}), 400
    new_todo = {"id": len(todos) + 1, "task": data["task"], "done": False}
    todos.append(new_todo)
    return jsonify(new_todo), 201


@app.route("/todos/<int:todo_id>/done", methods=["PUT"])
def mark_done(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return jsonify(todo)
    return jsonify({"error": "todo not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
