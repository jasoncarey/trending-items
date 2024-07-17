from confluent_kafka import Consumer, KafkaException, KafkaError
from heapq import heappush, heappushpop
import json
import math
import time

HEAP_SIZE: int = 20

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "heapGroup",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe(["interactions"])

heap = []


def calculate_score(interaction_time, current_time):
    decay_factor = 0.1
    time_diff = current_time - interaction_time
    return math.exp(-decay_factor * time_diff)


def add_to_heap(item):
    global heap
    if item is not None:
        print("item:", item)
        current_time = time.time()
        interaction_time = item.get("timestamp")
        score = calculate_score(interaction_time, current_time)
        print(f"Added to heap: {item}, score: {score}")
        heap_item = (score, item)
        if len(heap) < HEAP_SIZE:
            heappush(heap, heap_item)
        else:
            heappushpop(heap, heap_item)


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
            add_to_heap(interaction)
            print(f"heap state: {heap}")


def get_heap_data():
    print("heap:", heap)
    return [{"score": item[0], **item[1]} for item in heap]


if __name__ == "__main__":
    try:
        consume_messages()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
