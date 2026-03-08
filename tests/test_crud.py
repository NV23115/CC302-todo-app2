import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_task(client):
    # Arrange + Act
    response = client.post("/", data={"task": "Buy milk"}, follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "Buy milk" in response.get_data(as_text=True)


def test_update_task(client):
    # Arrange (create task first)
    client.post("/", data={"task": "Old task"}, follow_redirects=True)

    task_id = 0   # first item index

    # Act
    response = client.get(f"/toggle/{task_id}", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "Old task" in response.get_data(as_text=True)


def test_delete_task(client):
    client.post("/", data={"task": "Task to delete"}, follow_redirects=True)
    task_id = 0
    response = client.get(f"/delete/{task_id}", follow_redirects=True)

    # Only check status code
    assert response.status_code == 200