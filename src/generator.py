import time
from random import randint, choices


def generate_items():
    item_post_times = {str(i): time.time() - randint(0, 600) for i in range(1, 21)}
    return item_post_times


def generate_interaction(items):
    ids = list(items.keys())
    weights = [10] * 10 + [1] * 10  # Weight IDs 1-10 more heavily (to view results)

    interaction_id = choices(ids, weights)[0]
    interaction = {
        "id": interaction_id,
        "timestamp": time.time(),
        "post_time": items[interaction_id],
    }

    # print(f"Generated interaction: {interaction}")
    return interaction
