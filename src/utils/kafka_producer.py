from kafka import KafkaProducer
import json
import os


class OrderKafkaProducer:
    def __init__(self, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.topic = topic

    def send_order(self, order_data):
        self.producer.send(self.topic, order_data)
        self.producer.flush()
