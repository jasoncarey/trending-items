from heapq import heappush, heappushpop, heapify
import math
import time

BASE_DECAY_FACTOR = 0.1
HEAP_SIZE: int = 20
HEAP_LIFETIME = 600

heap = []
score_map = {}


def initialize_items_lut(items):
    global items_lut
    items_lut = items.copy()
    print(f"Items LUT: {items_lut}")


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

        heap_item = (score_map[interaction_id], interaction_id)

        if len(heap) < HEAP_SIZE:
            heappush(heap, heap_item)
        else:
            if score_map[interaction_id] > heap[0][0]:
                heappushpop(heap, heap_item)
        print(f"Added to heap: {heap_item}")


def decay_heap():
    global heap, score_map
    current_time = time.time()
    new_heap = []
    for _, interaction_id in heap:
        post_time = items_lut.get(interaction_id)
        if post_time is None:
            print(f"Skipping decay for {interaction_id} as post time is not found")
            continue
        decay_factor = calculate_decay_factor(post_time, current_time)
        new_score = score_map[interaction_id] * decay_factor
        score_map[interaction_id] = new_score
        new_heap.append((new_score, interaction_id))

    heap[:] = new_heap
    heapify(heap)
    print(f"Decayed heap: {heap}")


def get_heap_data():
    reversed_heap = sorted(heap, reverse=True)
    return [{"score": item[0], "id": item[1]} for item in reversed_heap]
