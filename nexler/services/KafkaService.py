from kafka import KafkaConsumer, KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from nexler.utils.config_util import Config


class KafkaService:
    def __init__(self):
        self.bootstrap_servers = f"{Config().get('KAFKA_HOST')}:{Config().get('KAFKA_PORT')}"
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        """
        Create a Kafka topic.
        """
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self.admin_client.create_topics([topic])
            print(f"Topic '{topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists.")
        except Exception as e:
            print(f"Failed to create topic '{topic_name}': {e}")

    def subscribe(self, topic_name, group_id=None, auto_offset_reset="earliest"):
        """
        Subscribe to a Kafka topic and consume messages.
        """
        try:
            consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                auto_offset_reset=auto_offset_reset
            )
            print(f"Subscribed to topic '{topic_name}'. Listening for messages...")
            for message in consumer:
                print(f"Received message: {message.value.decode('utf-8')}")
        except Exception as e:
            print(f"Failed to subscribe to topic '{topic_name}': {e}")

    def publish_message(self, topic_name, key=None, value=None):
        """
        Publish a message to a Kafka topic.
        """
        try:
            future = self.producer.send(topic_name, key=key, value=value)
            result = future.get(timeout=10)
            print(f"Message sent to topic '{topic_name}', partition {result.partition}, offset {result.offset}")
        except Exception as e:
            print(f"Failed to publish message to topic '{topic_name}': {e}")

    def close(self):
        """
        Close the Kafka producer and admin client.
        """
        self.producer.close()
        self.admin_client.close()
        print("Kafka connections closed.")
