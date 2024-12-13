from threading import Thread
import signal
from flask import Flask
from nexler.services import KafkaService
from nexler.utils import config_util

# Control flags and Kafka thread
is_running = False
kafka_thread = None


def consume_kafka_events():
    """Simulates consuming Kafka events in a separate thread."""
    global is_running
    kafka_service = KafkaService()
    kafka_topics = config_util.Config("app/config/KafkaTopics.json").get("topics")
    while is_running:
        for item in kafka_topics:
            kafka_service.subscribe(item.get("topic"), item.get("group"))


def start_kafka_thread():
    """Starts the Kafka consumer thread."""
    global is_running, kafka_thread
    is_running = True
    kafka_thread = Thread(target=consume_kafka_events, daemon=True)
    kafka_thread.start()
    print("Kafka consumer thread started.")


def stop_kafka_thread():
    """Stops the Kafka consumer thread."""
    global is_running, kafka_thread
    is_running = False
    if kafka_thread and kafka_thread.is_alive():
        kafka_thread.join()
    print("Kafka consumer thread stopped.")


def setup_kafka(app: Flask):
    """Configures Kafka thread lifecycle with the Flask app."""

    with app.app_context():
        """Start Kafka consumer if enabled in the configuration."""
        start_kafka_thread()

    @app.teardown_appcontext
    def cleanup_kafka(exception=None):
        """Stop Kafka consumer during app teardown."""
        stop_kafka_thread()

    # Signal handlers for Kubernetes or container environments
    def handle_shutdown_signal(signum, frame):
        print(f"Received signal {signum}, shutting down...")
        stop_kafka_thread()

    signal.signal(signal.SIGTERM, handle_shutdown_signal)
    signal.signal(signal.SIGINT, handle_shutdown_signal)
