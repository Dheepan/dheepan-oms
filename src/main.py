import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
from src.api.orders import router as orders_router
from src.database import get_db
from src.services.order_service import OrderService
from src.schemas.order import OrderUpdate
from typing import List, Optional


@strawberry.type
class OrderType:
    id: int
    customer_name: str
    product_name: str
    quantity: int
    price: float
    status: str


@strawberry.type
class Query:
    @strawberry.field
    def orders(self, info) -> List[OrderType]:
        db = next(get_db())
        order_service = OrderService(db)
        return order_service.list_orders()

    @strawberry.field
    def order(self, info, order_id: int) -> OrderType:
        db = next(get_db())
        order_service = OrderService(db)
        return order_service.get_order(order_id)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_order(
        self, info, customer_name: str, product_name: str, quantity: int, price: float
    ) -> OrderType:
        db = next(get_db())
        order_service = OrderService(db)
        order_data = {
            "customer_name": customer_name,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
        }
        order = order_service.create_order(order_data)
        return order

    @strawberry.mutation
    def update_order(
        self,
        info,
        order_id: int,
        customer_name: Optional[str] = None,
        product_name: Optional[str] = None,
        quantity: Optional[int] = None,
        price: Optional[float] = None,
        status: Optional[str] = None,
    ) -> OrderType:
        db = next(get_db())
        order_service = OrderService(db)
        order_data = {
            "customer_name": customer_name,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "status": status,
        }
        order_update = OrderUpdate(
            **{k: v for k, v in order_data.items() if v is not None}
        )
        order = order_service.update_order(order_id, order_update)
        return order

    @strawberry.mutation
    def delete_order(self, info, order_id: int) -> OrderType:
        db = next(get_db())
        order_service = OrderService(db)
        order = order_service.delete_order(order_id)
        return order


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders_router, prefix="/orders", tags=["orders"])

graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Management Microservice"}
