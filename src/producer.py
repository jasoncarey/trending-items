from confluent_kafka import Producer
import json
from interaction import generate_interaction
import time

conf = {"bootstrap.servers": "localhost:9092"}

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def produce_messages():
    while True:
        interaction = generate_interaction()
        print(f"Producing: {interaction}")
        producer.produce(
            "interactions",
            json.dumps(interaction).encode("utf-8"),
            callback=delivery_report,
        )
        producer.flush()
        time.sleep(1)


if __name__ == "__main__":
    produce_messages()
