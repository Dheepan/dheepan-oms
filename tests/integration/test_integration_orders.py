import pytest
from unittest.mock import patch, MagicMock


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

def test_create_and_get_order(mock_client, mock_db):
    # Mock order creation
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

    # Create order
    response = mock_client.post(
        "/orders/",
        json={"customer_name": "John Doe", "product_name": "Laptop", "quantity": 1, "price": 1000.0},
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "John Doe"
    assert response.json()["product_name"] == "Laptop"

    # Mock order retrieval
    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.json.return_value = mock_order

    # Get the created order
    response = mock_client.get("/orders/1")
    assert response.status_code == 200
    assert response.json()["customer_name"] == "John Doe"

def test_update_and_delete_order(mock_client, mock_db):
    # Mock order creation
    mock_order = {
        "id": 2,
        "customer_name": "Jane Doe",
        "product_name": "Phone",
        "quantity": 2,
        "price": 500.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = mock_order

    # Create order
    response = mock_client.post(
        "/orders/",
        json={"customer_name": "Jane Doe", "product_name": "Phone", "quantity": 2, "price": 500.0},
    )
    assert response.status_code == 200
    order_id = response.json()["id"]

    # Mock order update
    mock_updated_order = {
        "id": 2,
        "customer_name": "Jane Updated",
        "product_name": "Phone",
        "quantity": 2,
        "price": 500.0,
        "status": "pending"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    mock_client.put.return_value.status_code = 200
    mock_client.put.return_value.json.return_value = mock_updated_order

    # Update order
    response = mock_client.put(
        f"/orders/{order_id}",
        json={"customer_name": "Jane Updated", "product_name": "Phone", "quantity": 2, "price": 500.0},
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Jane Updated"

    # Mock order deletion
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    mock_db.commit.return_value = None

    mock_client.delete.return_value.status_code = 200

    # Delete order
    response = mock_client.delete(f"/orders/{order_id}")
    assert response.status_code == 200

    # Mock order retrieval after deletion
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_client.get.return_value.status_code = 404

    # Verify the order is deleted
    response = mock_client.get(f"/orders/{order_id}")
    assert response.status_code == 404