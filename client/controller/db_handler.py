from pymongo import MongoClient
from utils import get_env_variable

DB_URI = get_env_variable('DB_URI')
client = MongoClient(DB_URI)

def get_all_feedbacks():
    db = client['feedbacks']
    collection = db['feedbacks']
    all_feedbacks = collection.find()
    data = list(all_feedbacks)
    return data

def insert_feedback(feedback_data):
    username = feedback_data['username']
    user_id = feedback_data['user_id']
    feedback = feedback_data['feedback']
    date = feedback_data['date_time']

    db = client['feedbacks']
    collection = db['feedbacks']

    existing_user = collection.find_one({'user_id': user_id})

    if existing_user:
        collection.update_one(
            {'user_id': user_id},
            {'$push': {'feedbacks': {'feedback': feedback, 'date': date}}}
        )
    else:
        collection.insert_one({
            'user_id': user_id,
            'user_name': username,
            'feedbacks': [{'feedback': feedback, 'date': date}]
        })

