import json
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_get_todos(client):
    response = client.get("/todos")
    assert response.status_code == 200
    todos = response.get_json()
    assert isinstance(todos, list)
    assert len(todos) >= 2


def test_add_todo(client):
    new_todo = {"task": "测试添加任务"}
    response = client.post(
        "/todos", data=json.dumps(new_todo), content_type="application/json"
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["task"] == "测试添加任务"
    assert data["done"] is False


def test_add_todo_without_task(client):
    response = client.post(
        "/todos", data=json.dumps({}), content_type="application/json"
    )
    assert response.status_code == 400


def test_mark_done(client):
    response = client.put("/todos/1/done")
    assert response.status_code == 200
    data = response.get_json()
    assert data["done"] is True


def test_mark_done_not_found(client):
    response = client.put("/todos/9999/done")
    assert response.status_code == 404
