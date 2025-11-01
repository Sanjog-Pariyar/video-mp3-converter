import pika
import json
from app.config import settings

QUEUE_NAME = "video"

def publish_to_queue(message: dict, queue_name: str = QUEUE_NAME):
    """Publishes a message to the given RabbitMQ queue."""
    connection = None
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)

        body = json.dumps(message).encode("utf-8")
        channel.basic_publish(exchange="", routing_key=queue_name, body=body)

        print(f"📨 Sent message to '{queue_name}' queue: {message}")

    except Exception as e:
        print(f"❌ RabbitMQ publish failed: {e}")

    finally:
        if connection and connection.is_open:
            connection.close()