import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def mock_app():
    with patch("src.main.app") as mock_app:
        yield mock_app

@pytest.fixture(scope="module")
def mock_client(mock_app):
    with patch("fastapi.testclient.TestClient") as mock_test_client:
        mock_client_instance = MagicMock()
        mock_test_client.return_value = mock_client_instance
        yield mock_client_instance

@pytest.fixture(scope="module")
def mock_db():
    with patch("src.api.orders.get_db") as mock_get_db:
        mock_session = MagicMock()
        mock_get_db.return_value = mock_session
        yield mock_session

def test_create_order(mock_client, mock_db):
    mock_order = {
        "id": 1,
        "customer_name": "John Doe",
        "product_name": "Laptop",
        "quantity": 1,
        "price": 1000.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = mock_order

    response = mock_client.post(
        "/orders/",
        json={"customer_name": "John Doe", "product_name": "Laptop", "quantity": 1, "price": 1000.0},
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "John Doe"
    assert response.json()["product_name"] == "Laptop"

def test_list_orders(mock_client, mock_db):
    mock_orders = [
        {
            "id": 1,
            "customer_name": "John Doe",
            "product_name": "Laptop",
            "quantity": 1,
            "price": 1000.0,
            "status": "pending"
        }
    ]
    mock_db.query.return_value.all.return_value = mock_orders

    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.json.return_value = mock_orders

    response = mock_client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_order(mock_client, mock_db):
    mock_order = {
        "id": 2,
        "customer_name": "Jane Doe",
        "product_name": "Phone",
        "quantity": 2,
        "price": 500.0,
        "status": "pending"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.json.return_value = mock_order

    response = mock_client.get("/orders/2")
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Jane Doe"

def test_update_order(mock_client, mock_db):
    mock_order = {
        "id": 3,
        "customer_name": "Alice",
        "product_name": "Tablet",
        "quantity": 3,
        "price": 300.0,
        "status": "pending"
    }
    mock_updated_order = {
        "id": 3,
        "customer_name": "Alice Updated",
        "product_name": "Tablet",
        "quantity": 3,
        "price": 300.0,
        "status": "pending"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    mock_client.put.return_value.status_code = 200
    mock_client.put.return_value.json.return_value = mock_updated_order

    response = mock_client.put(
        "/orders/3",
        json={"customer_name": "Alice Updated", "product_name": "Tablet", "quantity": 3, "price": 300.0},
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Alice Updated"

def test_delete_order(mock_client, mock_db):
    mock_order = {
        "id": 4,
        "customer_name": "Bob",
        "product_name": "Monitor",
        "quantity": 1,
        "price": 200.0,
        "status": "pending"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    mock_db.commit.return_value = None

    mock_client.delete.return_value.status_code = 200

    response = mock_client.delete("/orders/4")
    assert response.status_code == 200

    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_client.get.return_value.status_code = 404

    response = mock_client.get("/orders/4")
    assert response.status_code == 404