from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)


class OrderKafkaConsumer:
    def __init__(self, topic: str, bootstrap_servers: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def consume_messages(self):
        for message in self.consumer:
            logging.info(f"Received message: {message.value}")
            self.process_message(message.value)

    def process_message(self, message):
        # Implement your message processing logic here
        pass


if __name__ == "__main__":
    consumer = OrderKafkaConsumer(
        topic="order_topic", bootstrap_servers="localhost:9092"
    )
    consumer.consume_messages()
