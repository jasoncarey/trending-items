from confluent_kafka import Producer
import json
import time
from generator import generate_interaction

conf = {"bootstrap.servers": "localhost:9092"}

producer = Producer(conf)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} topic in partition [{msg.partition()}]"
        )


def produce_messages(items):
    while True:
        interaction = generate_interaction(items)
        print(f"Producing: {interaction}")
        producer.produce(
            "interactions",
            json.dumps(interaction).encode("utf-8"),
            callback=delivery_report,
        )
        producer.flush()
        time.sleep(0.1)


if __name__ == "__main__":
    from generator import generate_items

    items = generate_items()
    produce_messages(items)
