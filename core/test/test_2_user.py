from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
# for testing purpose
mock_user_id = '61d465592026a42bfdac7204'


def test_get_not_existing_user():
    fake_user = "not-user"
    response = client.get(f"/users/{fake_user}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"user {fake_user} not found!"
    }


# creating a user
def test_create_user():
    response = client.post("/users/", json={"tableNumber": "test-number"})
    assert response.status_code == 201
    assert response.json() == {
        "_id": response.json()['_id'],
        "tableNumber": "test-number"
    }


# Updating table to A2
def test_update_user():
    response = client.put(f"/users/{mock_user_id}", json={"tableNumber": "update-test"})
    assert response.status_code == 200
    assert response.json() == {
        "_id": mock_user_id,
        "tableNumber": "update-test"
    }


def test_get_exist_user():
    response = client.get(f"/users/{mock_user_id}")
    assert response.status_code == 200
    assert response.json() == {
        "_id": mock_user_id,
        "tableNumber": "update-test"
    }

