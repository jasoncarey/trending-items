from confluent_kafka import Producer
import json
import time
from random import randint, choices

conf = {"bootstrap.servers": "localhost:9092"}

producer = Producer(conf)

item_post_times = {
    str(i): time.time() - randint(0, 600) for i in range(1, 21)
}  # generate random post times in the last 10 minutes


def generate_interaction():
    ids = list(item_post_times.keys())
    weights = [10] * 10 + [1] * 10  # Weight IDs 1-10 more heavily (to view results)

    interaction_id = choices(ids, weights)[0]
    interaction = {
        "id": interaction_id,
        "timestamp": time.time(),
        "post_time": item_post_times[interaction_id],
    }

    print(f"Generated interaction: {interaction}")
    return interaction


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(
            f"Message delivered to {msg.topic()} topic in partition [{msg.partition()}]"
        )


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
        time.sleep(0.01)


if __name__ == "__main__":
    produce_messages()
