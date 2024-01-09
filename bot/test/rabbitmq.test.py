import unittest
from unittest.mock import patch
from rabbitmq import send_feedback_to_rabbitmq

class TestRabbitMQ(unittest.TestCase):

    @patch('rabbitmq.pika.BlockingConnection')
    def test_send_feedback_to_rabbitmq(self, mock_connection):
        # Mock the connection and channel objects
        mock_channel = mock_connection.return_value.channel.return_value

        # Define the feedback message
        feedback = "This is a test feedback"

        # Call the function
        send_feedback_to_rabbitmq(feedback)

        # Assert that the connection was established with the correct parameters
        mock_connection.assert_called_once_with(pika.ConnectionParameters(
            host='your_queue_uri',
            port='your_queue_port',
            virtual_host='your_queue_user',
            credentials=pika.PlainCredentials('your_queue_user', 'your_queue_pass')
        ))

        # Assert that the channel was created and the queue was declared
        mock_channel.queue_declare.assert_called_once_with(queue='feedback_queue', exclusive=False)

        # Assert that the feedback message was published to the queue
        mock_channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='feedback_queue',
            body=feedback
        )

if __name__ == '__main__':
    unittest.main()