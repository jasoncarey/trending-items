from flask import Flask, jsonify, render_template
import threading
from heap import get_heap_data, decay_heap
from consumer_socket import consume_messages
from flask_socketio import SocketIO
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
    print("Starting consumer thread...")
    threading.Thread(target=consume_messages, args=(socketio,), daemon=True).start()
    print("Starting heap data emitter thread...")
    threading.Thread(target=emit_heap_data, daemon=True).start()
    print("Starting periodic decay thread...")
    threading.Thread(target=periodic_decay, daemon=True).start()
    print("Running Flask app...")
    socketio.run(app, host="127.0.0.1", port=5000)
