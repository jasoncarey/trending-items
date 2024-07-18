from confluent_kafka import Consumer, KafkaException, KafkaError, TopicPartition
from heap import add_to_heap, remove_from_heap, get_heap_data
import json
import time
import threading

WINDOW_SIZE = 60

CURRENT_CONSUMER_CONF = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "currentGroup",
    "auto.offset.reset": "latest",
}

OLD_CONSUMER_CONF = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "oldGroup",
    "auto.offset.reset": "latest",
}

current_consumer = Consumer(CURRENT_CONSUMER_CONF)
old_consumer = Consumer(OLD_CONSUMER_CONF)
current_consumer.subscribe(["interactions"])
old_consumer.subscribe(["interactions"])


def consume_current_messages(socketio):
    while True:
        msg = current_consumer.poll(timeout=1.0)
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
            interaction_id = interaction.get("id")
            add_to_heap(interaction_id)
            heap_data = get_heap_data()
            socketio.emit("update", heap_data, namespace="/")
            print(f"Added to heap: {interaction_id}")


def consume_old_messages(socketio):
    while True:
        msg = old_consumer.poll(timeout=1.0)
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
            if interaction is not None:
                interaction_id = interaction.get("id")
                remove_from_heap(interaction_id)
                heap_data = get_heap_data()
                socketio.emit("update", heap_data, namespace="/")
                print(f"Removed from heap: {interaction_id}")


def initialize_old_consumer():
    """Initialize the old consumer to start reading messages from the offset
    that is 1 minute earlier than the current offset."""
    time.sleep(WINDOW_SIZE)
    current_offset = get_current_offset()
    if current_offset is not None:
        offset_difference = calculate_offset_difference(WINDOW_SIZE)
        old_offset = current_offset - offset_difference
        if old_offset < 0:
            old_offset = 0
        old_consumer.assign([TopicPartition("interactions", 0, old_offset)])
        print(f"old offset: {old_offset}")
        print(f"Old consumer initialized to offset: {old_offset}")


# def get_current_offset():
#     partitions = [TopicPartition("interactions", 0)]
#     current_consumer.assign(partitions)
#     offsets = current_consumer.position(partitions)

#     if offsets:
#         current_offset = offsets[0].offset
#         print(f"current offset: {current_offset}")
#         return current_offset
#     return None


def get_current_offset():
    partitions = [TopicPartition("interactions", 0)]
    low, high = current_consumer.get_watermark_offsets(partitions[0])
    print(f"Watermark offsets for partition 0 - low: {low}, high: {high}")
    return high - 1


def calculate_offset_difference(time_diff_seconds):
    """Calculate the offset difference for the given time difference."""
    messages_per_second = 10
    return messages_per_second * time_diff_seconds


if __name__ == "__main__":
    initialize_old_consumer()

    threading.Thread(target=consume_current_messages, args=(None,), daemon=True).start()
    threading.Thread(target=consume_old_messages, daemon=True).start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        current_consumer.close()
        old_consumer.close()
