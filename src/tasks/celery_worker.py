from celery import Celery
import os

# Initialize Celery
celery_app = Celery(
    "order_management",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)


@celery_app.task
def process_order(order_id):
    # Logic to process the order
    print(f"Processing order: {order_id}")
    # Add your order processing logic here
    return f"Order {order_id} processed successfully."
