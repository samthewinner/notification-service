"""
Task Manager

The TaskManager class is responsible for managing
tasks that are added to the queue. It processes the
tasks by sending requests to the metadata service and
temporary storage based on the task type.
"""

import asyncio
import time

from http_proto import HTTPProto
from kafka import KafkaConsumer

from consts import METADATA_SERVICE_ENDPOINT, KAFKA_HOST, KAFKA_PORT


class TaskManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.tasks = []
        self.metadata_service = HTTPProto(METADATA_SERVICE_ENDPOINT)
        self.kafka_consumer = self.create_kafka_consumer()

    def create_kafka_consumer(self):
        for _ in range(5):
            try:
                consumer = KafkaConsumer(
                    bootstrap_servers=f"{KAFKA_HOST}:{KAFKA_PORT}",
                    value_serializer=lambda v: v.encode("utf-8"),
                )
                return consumer
            except Exception as e:
                print(f"Failed to connect to Kafka: {e}")
                time.sleep(2)  # Wait before retrying
        print("Could not connect to Kafka after multiple attempts")

    def consume_messages_every_n_seconds(self, n: int = 1):
        while True:
            self.consume_messages()

    def consume_messages(self):
        for message in self.kafka_consumer:
            # TODO: Process message and add them to the RabbitQueue
            # Process:
            # 1. get the message
            # 2. fetch subscriber list
            # 3. divide the subscriber list into predefined chunk with message
            # 4. push new task to rabbit queue

            topic = message.topic
            message = message.value.decode("utf-8")

            # call metadata service to get subscriber list
            subscriber_list = self.metadata_service.get_subscriber_list(topic)

            print(f"Received message: {message.value}")
