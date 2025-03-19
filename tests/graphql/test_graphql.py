import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="module")
def mock_app():
    with patch("src.main.graphql_app") as mock_app:
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
    query = """
    mutation {
        createOrder(customerName: "John Doe", productName: "Laptop", quantity: 1, price: 1000.0) {
            id
            customerName
            productName
            quantity
            price
            status
        }
    }
    """
    mock_order = {
        "id": 1,
        "customerName": "John Doe",
        "productName": "Laptop",
        "quantity": 1,
        "price": 1000.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"createOrder": mock_order}}

    response = mock_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json()["data"]["createOrder"]["customerName"] == "John Doe"
    assert response.json()["data"]["createOrder"]["productName"] == "Laptop"

def test_list_orders(mock_client, mock_db):
    query = """
    query {
        orders {
            id
            customerName
            productName
            quantity
            price
            status
        }
    }
    """
    mock_orders = [
        {
            "id": 1,
            "customerName": "John Doe",
            "productName": "Laptop",
            "quantity": 1,
            "price": 1000.0,
            "status": "pending"
        }
    ]
    mock_db.query.return_value.all.return_value = mock_orders

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"orders": mock_orders}}

    response = mock_client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert len(response.json()["data"]["orders"]) > 0

def test_get_order(mock_client, mock_db):
    create_query = """
    mutation {
        createOrder(customerName: "Jane Doe", productName: "Phone", quantity: 2, price: 500.0) {
            id
        }
    }
    """
    mock_order = {
        "id": 2,
        "customerName": "Jane Doe",
        "productName": "Phone",
        "quantity": 2,
        "price": 500.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"createOrder": mock_order}}

    create_response = mock_client.post("/graphql", json={"query": create_query})
    order_id = create_response.json()["data"]["createOrder"]["id"]

    get_query = f"""
    query {{
        order(orderId: {order_id}) {{
            id
            customerName
            productName
            quantity
            price
            status
        }}
    }}
    """
    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"order": mock_order}}

    response = mock_client.post("/graphql", json={"query": get_query})
    assert response.status_code == 200
    assert response.json()["data"]["order"]["customerName"] == "Jane Doe"

def test_update_order(mock_client, mock_db):
    create_query = """
    mutation {
        createOrder(customerName: "Alice", productName: "Tablet", quantity: 3, price: 300.0) {
            id
        }
    }
    """
    mock_order = {
        "id": 3,
        "customerName": "Alice",
        "productName": "Tablet",
        "quantity": 3,
        "price": 300.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"createOrder": mock_order}}

    create_response = mock_client.post("/graphql", json={"query": create_query})
    order_id = create_response.json()["data"]["createOrder"]["id"]

    update_query = f"""
    mutation {{
        updateOrder(orderId: {order_id}, customerName: "Alice Updated", productName: "Tablet", quantity: 3, price: 300.0) {{
            id
            customerName
            productName
            quantity
            price
            status
        }}
    }}
    """
    mock_updated_order = {
        "id": 3,
        "customerName": "Alice Updated",
        "productName": "Tablet",
        "quantity": 3,
        "price": 300.0,
        "status": "pending"
    }
    mock_db.query.return_value.filter.return_value.first.return_value = mock_updated_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"updateOrder": mock_updated_order}}

    response = mock_client.post("/graphql", json={"query": update_query})
    assert response.status_code == 200
    assert response.json()["data"]["updateOrder"]["customerName"] == "Alice Updated"

def test_delete_order(mock_client, mock_db):
    create_query = """
    mutation {
        createOrder(customerName: "Bob", productName: "Monitor", quantity: 1, price: 200.0) {
            id
        }
    }
    """
    mock_order = {
        "id": 4,
        "customerName": "Bob",
        "productName": "Monitor",
        "quantity": 1,
        "price": 200.0,
        "status": "pending"
    }
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"createOrder": mock_order}}

    create_response = mock_client.post("/graphql", json={"query": create_query})
    order_id = create_response.json()["data"]["createOrder"]["id"]

    delete_query = f"""
    mutation {{
        deleteOrder(orderId: {order_id}) {{
            id
        }}
    }}
    """
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order
    mock_db.delete.return_value = None
    mock_db.commit.return_value = None

    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"deleteOrder": {"id": order_id}}}

    response = mock_client.post("/graphql", json={"query": delete_query})
    assert response.status_code == 200

    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_client.post.return_value.status_code = 200
    mock_client.post.return_value.json.return_value = {"data": {"order": None}}

    get_query = f"""
    query {{
        order(orderId: {order_id}) {{
            id
        }}
    }}
    """
    response = mock_client.post("/graphql", json={"query": get_query})
    assert response.status_code == 200
    assert response.json()["data"]["order"] is None