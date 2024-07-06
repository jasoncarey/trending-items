from kafka import KafkaConsumer
import json
from heapq import heappush, heappop, heapify

consumer = KafkaConsumer(
    'interactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

heap = heapify([])

def add_to_heap(item):
    if len(heap) < 100:
        heappush(heap, item)
    else:
        heappop(heap)
        heappush(heap, item)

def consume_messages():
    for message in consumer:
        interaction = message.value
        add_to_heap(interaction)
        print(f"Consumed: {interaction}")

if __name__ == '__main__':
    consume_messages()