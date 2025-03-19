from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services.order_service import OrderService
from src.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from src.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.create_order(order.dict())


@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.list_orders()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    return order_service.get_order(order_id)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int, order: OrderUpdate, db: Session = Depends(get_db)
):
    order_service = OrderService(db)
    updated_order = await order_service.update_order(order_id, order)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_service = OrderService(db)
    success = await order_service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}
