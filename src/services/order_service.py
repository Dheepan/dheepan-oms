from sqlalchemy.orm import Session
from src.models.order import Order
from src.schemas.order import OrderCreate, OrderUpdate


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: dict):
        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def list_orders(self):
        return self.db.query(Order).all()

    def update_order(self, order_id: int, order_data: OrderUpdate):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            for key, value in order_data.dict(exclude_unset=True).items():
                setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
        return order

    def delete_order(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            self.db.delete(order)
            self.db.commit()
        return order
