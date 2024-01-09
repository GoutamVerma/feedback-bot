import pika
from typing import Final
from utils import get_env_variable

QUEUE_URI: Final = get_env_variable('QUEUE_URI')
QUEUE_PORT: Final = get_env_variable('QUEUE_PORT')
QUEUE_USER: Final = get_env_variable('QUEUE_USER')
QUEUE_PASS: Final = get_env_variable('QUEUE_PASS')

def send_feedback_to_rabbitmq(feedback: str) -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=QUEUE_URI,
        port=QUEUE_PORT,
        virtual_host=QUEUE_USER,
        credentials=pika.PlainCredentials(QUEUE_USER, QUEUE_PASS)
    ))
    with connection:
        channel = connection.channel()
        channel.queue_declare(queue='feedback_queue',exclusive=False)
        channel.basic_publish(exchange='', routing_key='feedback_queue', body=feedback)
