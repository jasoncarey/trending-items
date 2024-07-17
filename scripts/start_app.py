import subprocess
import sys


def start_producer():
    print("Starting Kafka producer...")
    producer_command = ["python3", "src/producer.py"]
    producer_process = subprocess.Popen(
        producer_command, stdout=sys.stdout, stderr=sys.stderr
    )
    print("Kafka producer started.")
    return producer_process


# def start_consumer_visualizer():
#     print("Starting Kafka consumer...")
#     consumer_command = ["python3", "src/consumer_socket.py"]
#     consumer_visualizer_process = subprocess.Popen(
#         consumer_command, stdout=sys.stdout, stderr=sys.stderr
#     )
#     print("Kafka consumer started.")
#     return consumer_visualizer_process


def start_visualizer():
    print("Starting Kafka visualizer...")
    visualizer_command = ["python3", "src/heap_visualizer.py"]
    visualizer_process = subprocess.Popen(
        visualizer_command, stdout=sys.stdout, stderr=sys.stderr
    )
    print("Kafka visualizer started.")
    return visualizer_process


def main():
    producer_process = start_producer()
    # consumer_visualizer_process = start_consumer_visualizer()
    visualizer_process = start_visualizer()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
        producer_process.terminate()
        # consumer_visualizer_process.terminate()
        visualizer_process.terminate()
        producer_process.wait()
        # consumer_visualizer_process.wait()
        visualizer_process.wait()
        print("All processes terminated.")
        sys.exit(0)


if __name__ == "__main__":
    main()
