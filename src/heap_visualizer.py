from flask import Flask, jsonify
from heapq import heappush, heappop, heapify
import threading
import time

app = Flask(__name__)

heap = []

@app.route('/heap', methods=['GET'])
def get_heap():
    return jsonify([item[1] for item in heap])

def add_to_heap(item):
    global heap
    heap_item = (item['timestamp'], item)
    if len(heap) < 100:
        heappush(heap, heap_item)
    else:
        heappop(heap)
        heappush(heap, heap_item)

def mock_interaction_data():
    while True:
        item = {
            'item_id': f'item_{time.time()}',
            'timestamp': time.time()
        }
        add_to_heap(item)
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=mock_interaction_data).start()
    app.run(port=5000)