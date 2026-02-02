"""
RabbitMQ queue utilities
"""
import pika
import json
import logging

from company_insight_service.config.settings import settings

logger = logging.getLogger(__name__)


def publish_to_queue(data: dict):
    """
    Publish data to RabbitMQ queue
    
    Args:
        data: Dictionary to publish to queue
    """
    try:
        params = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key=settings.RABBITMQ_QUEUE_NAME,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        connection.close()
        logger.info(f"Published message to queue: {settings.RABBITMQ_QUEUE_NAME}")
        
    except Exception as e:
        logger.error(f"Failed to publish to queue: {e}")
        raise
