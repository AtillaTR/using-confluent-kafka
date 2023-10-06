from confluent_kafka import Producer
import socket
import requests
import json


def get_credentials() -> str:
    with open('connection_credentials.json', 'r') as file:

        cred = json.load(file)

        BOOTSTRAP_SERVERS = cred['bootstrap_server']
        CLIENT_ID = cred['client_id']

        return BOOTSTRAP_SERVERS, CLIENT_ID


def wikimedia_producer(BOOTSTRAP_SERVERS: str, CLIENT_ID: str, TOPIC: str, value: str, key: str = "null"):
    conf = {'bootstrap.servers': BOOTSTRAP_SERVERS,
            'client.id': CLIENT_ID}

    producer = Producer(conf)
    producer.produce(TOPIC, key=key, value=value, callback=acked)
    producer.poll(1)
    producer.flush()


def acked(err: object, msg: object):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


if __name__ == "__main__":

    BOOTSTRAP_SERVERS, CLIENT_ID = get_credentials()
    TOPIC = 'wikimedia.recentchange'
    URL = 'https://stream.wikimedia.org/v2/stream/recentchange'

    response = requests.get(URL, stream=True)

    for line in response.iter_lines():
        if 'data:' in str(line):
            wikimedia_producer(BOOTSTRAP_SERVERS, CLIENT_ID, TOPIC, line)
