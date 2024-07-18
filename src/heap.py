from heapq import heappush, heappushpop, heapify
import math
import time
import threading
import collections

BASE_DECAY_FACTOR = 0.1
HEAP_SIZE: int = 20
HEAP_LIFETIME = 600

heap = []
counts = collections.defaultdict(int)
lock = threading.Lock()


def add_to_heap(id):
    global heap, counts
    with lock:
        counts[id] += 1

    item = (counts[id], id)

    if id in [i[1] for i in heap]:
        heap = [(s, i) for s, i in heap if i != id]
        heapify(heap)

    if len(heap) < HEAP_SIZE:
        heappush(heap, item)
    else:
        if counts[id] > heap[0][0]:
            heappushpop(heap, item)


def remove_from_heap(id):
    global heap, counts
    with lock:
        counts[id] -= 1
        if counts[id] <= 0:
            del counts[id]
            heap = [(s, i) for s, i in heap if i != id]
            heapify(heap)
        else:
            heap = [(s, i) for s, i in heap if id != id]
            item = (counts[id], id)
            heappush(heap, item)
            heapify(heap)


def get_heap_data():
    reversed_heap = sorted(heap, reverse=True)
    return [{"score": item[0], "id": item[1]} for item in reversed_heap]


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


def initialize_items_lut(items):
    global items_lut
    items_lut = items.copy()
    print(f"Items LUT: {items_lut}")


def calculate_decay_factor(post_time, current_time):
    time_since_post = current_time - post_time
    return math.exp(-BASE_DECAY_FACTOR * time_since_post)
