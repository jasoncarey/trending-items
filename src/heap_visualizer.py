from flask import Flask, jsonify, render_template
import threading
from heap import get_heap_data, decay_heap, initialize_items_lut
from producer import produce_messages
from flask_socketio import SocketIO
from consumer import (
    consume_current_messages,
    consume_old_messages,
    initialize_old_consumer,
)
import time

app = Flask(__name__)
socketio = SocketIO(app)

heap = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/heap", methods=["GET"])
def get_heap():
    return jsonify(get_heap_data())


def emit_heap_data():
    while True:
        heap_data = get_heap_data()
        socketio.emit("update", heap_data, namespace="/")
        print(f"Emitted heap data: {heap_data}")
        time.sleep(10)


def periodic_decay():
    while True:
        print("Decaying heap...")
        decay_heap()
        time.sleep(10)


if __name__ == "__main__":
    from generator import generate_items

    items = generate_items()
    initialize_items_lut(items)
    print(f"Items: {items}")

    initialize_old_consumer()
    threading.Thread(
        target=consume_current_messages, args=(socketio,), daemon=True
    ).start()
    threading.Thread(target=consume_old_messages, args=(socketio,), daemon=True).start()
    threading.Thread(target=produce_messages, args=(items,), daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000)
