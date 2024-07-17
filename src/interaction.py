import time
import uuid

def generate_interaction():
    return {
        'id': str(uuid.uuid4()),
        'timestamp': time.time()
    }
