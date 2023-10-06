

# Kafka and OpenSearch Integration Project

This project aims to demonstrate efficient integration between Apache Kafka and OpenSearch (formerly known as Elasticsearch) for real-time data processing and indexing from the Wikimedia RecentChange event stream. The project consists of two main components: a Kafka consumer and a Kafka producer.

## Kafka Consumer

The Kafka consumer is responsible for receiving messages from a Kafka topic (in this case, 'wikimedia.recentchange'), processing them, and indexing them in an OpenSearch index. Here's how it works:

### Dependencies

- **confluent_kafka**: This library is used to create a Kafka consumer that subscribes to Kafka topics and consumes messages.

- **OpenSearch (opensearchpy)**: The `OpenSearch` class is used to establish a connection with the OpenSearch cluster, and the `index` method is used to index messages in OpenSearch.

### Features

1. **Connection Setup**: The `create_open_search_client` function establishes a connection with the OpenSearch cluster at 'http://localhost:9200'. If successful, it returns an OpenSearch client object.

2. **Kafka Consumer Configuration**: The `create_kafka_consumer` function configures a Kafka consumer with necessary settings, including the Kafka server ('localhost:9092'), group ID, session timeout, and offset reset behavior.

3. **Message Processing**: The `consume_loop` function continuously polls for messages from the Kafka topic. When a message is received, it decodes it, and relevant information is extracted.

4. **Indexing into OpenSearch**: Extracted message data is indexed into the OpenSearch index named 'wikimedia'. If indexing is successful, the message is acknowledged.

5. **Offset Committing**: The consumer commits offsets periodically to ensure that message processing progress is saved. This is done every `MIN_COMMIT_COUNT` messages.

### Running the Consumer

To run the Kafka consumer, follow these steps:

1. **Make sure that the `docker-compose-kafka.yml` and `docker-compose-elasticsearch.yml` files are in the same directory as your project.

2. **Open a terminal and navigate to the project directory.

3. **Execute the following command to start the Kafka container**:

   ```bash
   docker-compose -f docker-compose-kafka.yml up -d
   ```

   This will start the Kafka containers in the background.

4. **Execute the following command to start the OpenSearch container**:

   ```bash
   docker-compose -f docker-compose-elasticsearch.yml up -d
   ```

   This will start the OpenSearch container in the background.

Now, the Kafka and OpenSearch containers are up and ready to be used by your project. Ensure they are functioning correctly before running your project's Python scripts. You can check the status of the containers using the `docker ps` command.

## Kafka Producer

The Kafka producer is responsible for fetching real-time data from the Wikimedia RecentChange event stream and publishing it to the Kafka topic. Here's how it works:

### Dependencies

- **confluent_kafka**: This library is used to create a Kafka producer that sends messages to the Kafka topic.

### Features

1. **Getting Credentials**: The `get_credentials` function reads connection credentials (Bootstrap Servers and Client ID) from a JSON file ('connection_credentials.json').

2. **Wikimedia Data Stream**: The script fetches real-time data from the Wikimedia RecentChange event stream ('https://stream.wikimedia.org/v2/stream/recentchange').

3. **Publishing to Kafka**: Each line of data fetched from the stream is treated as a message and published to the Kafka topic 'wikimedia.recentchange' using the `wikimedia_producer` function.

4. **Message Acknowledgment**: The producer acknowledges the success or failure of message delivery using the `acked` callback.

### Running the Producer

To run the Kafka producer, follow these steps:

1. **Ensure you have the required libraries installed** and provide the connection credentials in 'connection_credentials.json'.

2. **Execute the script** to start fetching and publishing data to the Kafka topic.

This project demonstrates a basic setup for integrating Kafka and OpenSearch for real-time data processing and indexing. In practice, you can extend and optimize this configuration to meet specific requirements and handle more complex use cases.

---
