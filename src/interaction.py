import time
import uuid


def generate_interaction():
    interaction = {"id": str(uuid.uuid4()), "timestamp": time.time()}
    # print(f"Produced interaction: {interaction}")
    return interaction
