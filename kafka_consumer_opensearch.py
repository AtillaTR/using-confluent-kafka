from opensearchpy import OpenSearch
from confluent_kafka import Consumer, KafkaError, KafkaException
from opensearchpy.exceptions import RequestError
import sys
import json


running = True
MIN_COMMIT_COUNT = 100


def create_open_search_client() -> object:
    try:
        conn_string = "http://localhost:9200"
        os_client = OpenSearch(
            hosts=[conn_string],
            use_ssl=False

        )
        print("Opensearch connection successed.")

        return os_client
    except:
        print("Opensearch connection failed.")


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


def create_kafka_consumer() -> object:
    try:
        conf = {'bootstrap.servers': 'localhost:9092',
                'group.id': 'wikimedia-consumer',
                'session.timeout.ms': 6000,
                'on_commit': commit_completed,
                'auto.offset.reset': 'earliest'}

        kafka_consumer = Consumer(conf)
        print("The kafka consumer has been conected!")
        return kafka_consumer
    except:
        print("Opensearch connection failed.")

def extractId(message_dict:json)->str:
    return message_dict["data"]["meta"]["id"]

def consume_loop(consumer, topics, os_client):
    try:
        consumer.subscribe(topics)

        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(f'%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n')
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                message_json = msg.value().decode('utf-8')[5:]
                formatted_json = f'{{"data": {message_json}}}'
                message_dict = json.loads(formatted_json)
                message_id = extractId(message_dict)
                try:
                        response = os_client.index(
                            index=index_name, body=message_dict, id=message_id)
                        if response["result"] == "created" or response["result"] == "updated":
                            message_id = response["_id"]
                            print(f"Message indexed successfuly! MessageID: {message_id}")
                        else:
                            print("Message indexing have been failed.")
                except RequestError as e:
                    print(f"An error occurred while indexing: {e}")
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    TOPIC = ['wikimedia.recentchange']
    index_name = "wikimedia"
    index_mapping = {
        "mappings": {
            "properties": {
                "data": {
                    "type": "object"
                }
            }
        }
    }
    os_client = create_open_search_client()
    response = os_client.indices.exists(index=index_name)
    if not response:
        response = os_client.indices.create(index_name, body=index_mapping)
        print("The Wikimedia index has been created!")
    print("The Wikimedia index already exists.")

    kafka_consumer = create_kafka_consumer()
    consume_loop(kafka_consumer, TOPIC, os_client)
