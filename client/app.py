import pika
import json
import logging
from flask import Flask, render_template, jsonify 
from flask_socketio import SocketIO
from utils import get_env_variable
from controller.db_handler import insert_feedback, get_all_feedbacks


app = Flask(__name__)
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration variables
QUEUE_URI = get_env_variable('QUEUE_URI')
QUEUE_PORT = get_env_variable('QUEUE_PORT')
QUEUE_USER = get_env_variable('QUEUE_USER')
QUEUE_PASS = get_env_variable('QUEUE_PASS')

# RabbitMQ connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=QUEUE_URI,
    port=QUEUE_PORT,
    virtual_host=QUEUE_USER,
    credentials=pika.PlainCredentials(QUEUE_USER, QUEUE_PASS)
))
channel = connection.channel()


@app.route('/')
def live_feedbacks():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/feedbacks')
def feedbacks():
    """Render the feedbacks.html template with all feedbacks."""
    data = get_all_feedbacks()
    return render_template('feedbacks.html', feedback_list=data)

def background_thread():
    """Continuously listen for new messages from the feedback_queue."""
    while True:
        method_frame, _, body = channel.basic_get(queue='feedback_queue', auto_ack=True)
        if method_frame:
            message = json.loads(body.decode('utf-8'))
            insert_feedback(message)
            socketio.emit('new_message', {'message': message})
        socketio.sleep(1)  


@socketio.on('connect')
def handle_connect():
    """Handle the connection event."""
    socketio.emit('connection_response', {'data': 'Connected'})
    socketio.start_background_task(target=background_thread)


@app.route("/hello", methods=["GET"])
def say_hello():
    return jsonify({"msg": "Hello from Flask"})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
