from pymongo import MongoClient
from kafka import KafkaProducer
import json

mongo_client = MongoClient('localhost', 27017)
db = mongo_client['trending-db']
collection = db['interactions']

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'], 
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def listen_to_changes():
    try:
        with collection.watch() as stream:
            for change in stream:
                if change['operationType'] == 'insert':
                    document = change['fullDocument']
                    producer.send('interactions', document)
                    print(f"Produced: {document}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    listen_to_changes()

