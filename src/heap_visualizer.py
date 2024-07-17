from flask import Flask, jsonify, render_template
import threading
from consumer_heap import get_heap_data
from consumer_socket import consume_messages
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

heap = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/heap", methods=["GET"])
def get_heap():
    return jsonify(get_heap_data())


if __name__ == "__main__":
    threading.Thread(target=consume_messages, args=(socketio,), daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000)
