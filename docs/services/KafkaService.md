## Kafka Service Documentation

This documentation provides guidance on setting up and using the Kafka service in a Python-based application, leveraging Kafka for messaging and event processing. This includes instructions for enabling Kafka, creating topics, subscribing to topics, and publishing messages using the `KafkaService` class.

### Enabling Kafka in the Application

To enable Kafka, you need to add the following configuration to your environment settings (e.g., `.env` file or environment variables):

```ini
# Kafka Configuration
KAFKA=on
KAFKA_HOST=localhost
KAFKA_PORT=9092
```

- `KAFKA`: Set this to `on` to enable Kafka support in your application.
- `KAFKA_HOST`: The hostname or IP address of your Kafka broker (e.g., `localhost` for local development).
- `KAFKA_PORT`: The port where Kafka is running (default is `9092`).

### KafkaService Class

The `KafkaService` class encapsulates common Kafka operations such as creating topics, subscribing to topics, and publishing messages. This class interacts with the Kafka broker using the `KafkaConsumer`, `KafkaProducer`, and `KafkaAdminClient` from the `kafka-python` library.

#### KafkaService Class Methods

1. **`__init__(self)`**  
   Initializes the Kafka client connections (producer, consumer, and admin) using the configuration from `Config`.

   ```python
   def __init__(self):
       self.bootstrap_servers = f"{Config().get('KAFKA_HOST')}:{Config().get('KAFKA_PORT')}"
       self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
       self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
   ```

2. **`create_topic(self, topic_name, num_partitions=1, replication_factor=1)`**  
   Creates a new Kafka topic. If the topic already exists, it prints an error message.

   Parameters:
   - `topic_name`: The name of the topic to create.
   - `num_partitions`: The number of partitions for the topic (default is 1).
   - `replication_factor`: The replication factor for the topic (default is 1).

   Example usage:
   ```python
   kafka_service.create_topic('my_topic', 3, 2)
   ```

3. **`subscribe(self, topic_name, group_id=None, auto_offset_reset="earliest")`**  
   Subscribes to a Kafka topic and consumes messages. The consumer listens to the topic and processes messages in real-time.

   Parameters:
   - `topic_name`: The name of the topic to subscribe to.
   - `group_id`: The consumer group ID (optional).
   - `auto_offset_reset`: Specifies what to do when there is no initial offset (default is `"earliest"`).

   Example usage:
   ```python
   kafka_service.subscribe('my_topic', 'my_group')
   ```

4. **`publish_message(self, topic_name, key=None, value=None)`**  
   Publishes a message to a Kafka topic. Optionally, you can specify a message key and value.

   Parameters:
   - `topic_name`: The name of the Kafka topic to send the message to.
   - `key`: The key for the Kafka message (optional).
   - `value`: The value (payload) of the message.

   Example usage:
   ```python
   kafka_service.publish_message('my_topic', key='key1', value='Hello Kafka!')
   ```

5. **`close(self)`**  
   Closes the Kafka producer and admin client connections gracefully.

   Example usage:
   ```python
   kafka_service.close()
   ```

### Example Usage of KafkaService

```python
from nexler.services import KafkaService

# Initialize Kafka service
kafka_service = KafkaService()

# Create a Kafka topic
kafka_service.create_topic('my_topic', num_partitions=3, replication_factor=2)

# Subscribe to a Kafka topic
kafka_service.subscribe('my_topic', group_id='my_group')

# Publish a message to a Kafka topic
kafka_service.publish_message('my_topic', key='key1', value='Hello Kafka!')

# Close Kafka connections
kafka_service.close()
```

### Automation of KafkaService
With `do_something()` function in `kafkaActions` folder you can enable automated listening according to topics mentioned in `kafkaTopics.json` inside config folder. 

### Troubleshooting

- **`TopicAlreadyExistsError`**: If you encounter this error while creating a topic, it means the topic already exists. You can catch this error and handle it gracefully as shown in the `create_topic` method.
- **Connection Issues**: Ensure that the `KAFKA_HOST` and `KAFKA_PORT` values are correctly configured in your environment settings, and that Kafka is running and accessible at those addresses.

### Notes

1. **Kafka Version**: This implementation assumes you are using `kafka-python`, which supports a variety of Kafka versions. Ensure your Kafka instance is compatible with the client library.
   
2. **Scaling Kafka**: For production environments, consider setting up multiple partitions and replication for fault tolerance and performance.

3. **Graceful Shutdown**: Ensure that you close Kafka producer and consumer clients gracefully, especially in production environments, to avoid memory leaks or partial message sends.

---

This documentation covers basic usage, configuration, and error handling for Kafka in your application. For more advanced Kafka configurations and optimizations (e.g., tuning Kafka producer/consumer settings, handling message serialization), refer to the [Kafka Python documentation](https://kafka-python.readthedocs.io/en/master/).