from confluent_kafka import Consumer, KafkaException, KafkaError
from pymongo import MongoClient
import json

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "mongodbGroup",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["interactions"]
collection = db["interactions"]

consumer.subscribe(["interactions"])


def consume_messages():
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(
                    f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}"
                )
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            interaction = json.loads(msg.value().decode("utf-8"))
            collection.insert_one(interaction)
            print(f"Inserted: {interaction}")


if __name__ == "__main__":
    try:
        consume_messages()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
