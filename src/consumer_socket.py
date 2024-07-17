from confluent_kafka import Consumer, KafkaException, KafkaError
from consumer_heap import add_to_heap, get_heap_data
import json


def consume_messages(socketio):
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "heapGroup",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)
    consumer.subscribe(["interactions"])

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
            try:
                interaction = json.loads(msg.value().decode("utf-8"))
                add_to_heap(interaction)
                socketio.emit("update", get_heap_data(), namespace="/")
                print(f"Consumed: {interaction}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
