from heapq import heappush, heappushpop, heapify
import math
import time

BASE_DECAY_FACTOR = 0.1
HEAP_SIZE: int = 20
HEAP_LIFETIME = 600  # 10 minutes
heap = []
score_map = {}


def calculate_decay_factor(post_time, current_time):
    time_since_post = current_time - post_time
    return math.exp(-BASE_DECAY_FACTOR * time_since_post)


def add_to_heap(item):
    global heap, score_map
    print(f"Adding to heap: {item}")
    if item is not None:
        current_time = time.time()
        interaction_id = item.get("id")
        post_time = item.get("post_time")

        score = 1 * calculate_decay_factor(post_time, current_time)

        if interaction_id in score_map:
            score_map[interaction_id] += score
        else:
            score_map[interaction_id] = score

        heap_item = (score_map[interaction_id], item)

        if len(heap) < HEAP_SIZE:
            heappush(heap, heap_item)
        else:
            heappushpop(heap, heap_item)
        print(f"Added to heap: {heap_item}")

        heap = [
            (score, item)
            for score, item in heap
            if (current_time - item.get("timestamp")) < HEAP_LIFETIME
        ]
        heapify(heap)


def decay_heap():
    global heap, score_map
    current_time = time.time()
    new_heap = []
    for score, item in heap:
        post_time = item.get("post_time")
        if post_time is None:
            continue
        decay_factor = calculate_decay_factor(post_time, current_time)
        new_score = score_map[item.get("id")] * decay_factor
        score_map[item.get("id")] = new_score
        new_heap.append((new_score, item))
    heap[:] = new_heap
    heapify(heap)
    print(f"Decayed heap: {heap}")


def get_heap_data():
    return [{"score": item[0], **item[1]} for item in heap]
