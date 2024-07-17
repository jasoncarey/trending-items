import subprocess
import time
import os
import sys


def start_zookeeper():
    print("Starting Zookeeper...")
    zk_command = [
        "/opt/homebrew/bin/zookeeper-server-start",
        "/opt/homebrew/etc/zookeeper/zoo.cfg",
    ]
    zk_log = open("zookeeper.log", "w")
    zk_process = subprocess.Popen(zk_command, stdout=zk_log, stderr=subprocess.PIPE)
    print("Zookeeper started.")
    return zk_process, zk_log


def start_kafka():
    print("Starting Kafka...")
    kafka_command = [
        "/opt/homebrew/bin/kafka-server-start",
        "/opt/homebrew/etc/kafka/server.properties",
    ]
    kafka_log = open("kafka.log", "w")
    kafka_process = subprocess.Popen(
        kafka_command, stdout=kafka_log, stderr=subprocess.PIPE
    )
    print("Kafka started.")
    return kafka_process, kafka_log


def kafka_health_check():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 9092))
        s.close()
        return True
    except socket.error as e:
        print(f"Kafka health check failed: {e}")
        return False


def wait_for_kafka():
    print("Awaiting Kafka...")
    for i in range(30):
        if kafka_health_check():
            print("Kafka is ready.")
            return
        time.sleep(1)
    print("Kafka did not start in time. Exiting...")
    sys.exit(1)


def start_producer():
    print("Starting Kafka producer...")
    producer_command = ["python3", "src/producer.py"]
    producer_process = subprocess.Popen(
        producer_command, stdout=sys.stdout, stderr=sys.stderr
    )
    print("Kafka producer started.")
    return producer_process


def start_consumer():
    print("Starting Kafka consumer...")
    consumer_command = ["python3", "src/consumer_socket.py"]
    consumer_process = subprocess.Popen(
        consumer_command, stdout=sys.stdout, stderr=sys.stderr
    )
    print("Kafka consumer started.")
    return consumer_process


def start_visualizer():
    print("Starting Kafka visualizer...")
    visualizer_command = ["python3", "src/heap_visualizer.py"]
    visualizer_process = subprocess.Popen(
        visualizer_command, stdout=sys.stdout, stderr=sys.stderr
    )
    print("Kafka visualizer started.")
    return visualizer_process


def monitor_logs(zk_process, kafka_process):
    while True:
        zk_line = zk_process.stderr.readline()
        kafka_line = kafka_process.stderr.readline()

        if zk_line:
            print("[Zookeeper ERROR]:", zk_line.decode(), end="")
        if kafka_line:
            print("[Kafka ERROR]:", kafka_line.decode(), end="")


def main():
    zk_process, zk_log = start_zookeeper()
    time.sleep(10)

    kafka_process, kafka_log = start_kafka()
    time.sleep(10)

    wait_for_kafka()

    producer_process = start_producer()
    consumer_process = start_consumer()
    visualizer_process = start_visualizer()

    try:
        monitor_logs(zk_process, kafka_process)
    except KeyboardInterrupt:
        print("Shutting down...")
        zk_process.terminate()
        kafka_process.terminate()
        producer_process.terminate()
        consumer_process.terminate()
        visualizer_process.terminate()
        zk_process.wait()
        kafka_process.wait()
        producer_process.wait()
        consumer_process.wait()
        visualizer_process.wait()
        zk_log.close()
        kafka_log.close()
        print("Shutdown complete.")


if __name__ == "__main__":
    main()
