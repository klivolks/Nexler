from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from app.kafkaActions import do_something
from nexler.utils.config_util import Config


class KafkaService:
    def __init__(self):
        self.bootstrap_servers = f"{Config().get('KAFKA_HOST')}:{Config().get('KAFKA_PORT')}"
        self.admin_client = AdminClient({'bootstrap.servers': self.bootstrap_servers})
        self.producer = Producer({'bootstrap.servers': self.bootstrap_servers})

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        """
        Create a Kafka topic.
        """
        new_topic = NewTopic(topic_name, num_partitions, replication_factor)
        try:
            future = self.admin_client.create_topics([new_topic])
            for topic, result in future.items():
                try:
                    result.result()  # Wait for the topic to be created
                    print(f"Topic '{topic}' created successfully.")
                except KafkaException as e:
                    if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                        print(f"Topic '{topic}' already exists.")
                    else:
                        print(f"Failed to create topic '{topic}': {e}")
        except Exception as e:
            print(f"Unexpected error during topic creation: {e}")

    def subscribe(self, topic_name, group_id=None, auto_offset_reset="earliest"):
        """
        Subscribe to a Kafka topic and consume messages.
        """
        try:
            consumer_config = {
                'bootstrap.servers': self.bootstrap_servers,
                'group.id': group_id or 'default-group',
                'auto.offset.reset': auto_offset_reset,
                'enable.auto.commit': True
            }
            consumer = Consumer(consumer_config)
            consumer.subscribe([topic_name])

            print(f"Subscribed to topic '{topic_name}'. Listening for messages...")
            try:
                while True:
                    msg = consumer.poll(1.0)  # Poll for a message (timeout 1s)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            print(f"End of partition reached {msg.topic()} [{msg.partition()}]")
                        elif msg.error():
                            raise KafkaException(msg.error())
                    else:
                        do_something(msg.value().decode('utf-8'))
            except KeyboardInterrupt:
                print("Aborted by user.")
            finally:
                consumer.close()
        except Exception as e:
            print(f"Failed to subscribe to topic '{topic_name}': {e}")

    def publish_message(self, topic_name, key=None, value=None):
        """
        Publish a message to a Kafka topic.
        """
        try:
            key_bytes = key.encode('utf-8') if key else None
            value_bytes = value.encode('utf-8') if value else None
            self.producer.produce(topic=topic_name, key=key_bytes, value=value_bytes, callback=self.delivery_report)
            self.producer.flush()  # Ensures all messages are delivered
        except Exception as e:
            print(f"Failed to publish message to topic '{topic_name}': {e}")

    @staticmethod
    def delivery_report(err, msg):
        """Delivery report callback for produced messages."""
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

    def close(self):
        """
        Close the Kafka producer and admin client.
        """
        # The confluent_kafka producer does not require explicit closing
        print("KafkaService resources cleaned up.")
