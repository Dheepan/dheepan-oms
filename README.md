# Order Management Microservice - Work In Progress

This project is an Order Management Microservice built using FastAPI, Celery, Kafka, and GraphQL. It is designed to handle order-related operations in a scalable and efficient manner.

## Features

- FastAPI for building the API
- GraphQL endpoint for flexible queries
- Celery for background task processing
- Kafka for message brokering
- Docker for containerization

## Project Structure

```
order-management-microservice
├── src
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api                   # Contains API route definitions
│   │   ├── orders.py         # Order-related API endpoints
│   ├── models                # Contains data models
│   │   ├── order.py          # Order model definition
│   ├── schemas               # Contains Pydantic schemas
│   │   ├── order.py          # Order validation and serialization schemas
│   ├── services              # Contains business logic
│   │   ├── order_service.py   # Functions for managing orders
│   ├── tasks                 # Contains background tasks
│   │   ├── celery_worker.py   # Celery worker setup
│   ├── utils                 # Utility functions
│   │   ├── kafka_producer.py  # Kafka producer implementation
│   │   ├── kafka_consumer.py  # Kafka consumer implementation
├── Dockerfile                 # Docker image instructions
├── docker-compose.yml         # Docker services configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .env                       # Environment variables
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd order-management-microservice
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables in the `.env` file.

5. Build and run the application using Docker:
   ```
   docker-compose up --build
   ```

## Usage

- The FastAPI application will be available at `http://localhost:8000`.
- Access the GraphQL endpoint at `http://localhost:8000/graphql`.
- Use the API endpoints defined in `src/api/orders.py` for order management.

## API Endpoints

Refer to the API documentation for detailed information on available endpoints and their usage.

## License

This project is licensed under the MIT License.
