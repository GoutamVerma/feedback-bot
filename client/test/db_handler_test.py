import unittest
from unittest.mock import patch
from pymongo import MongoClient
from db_handler import get_all_feedbacks, insert_feedback

class TestDBHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient()
        cls.db = cls.client['feedbacks']
        cls.collection = cls.db['feedbacks']

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database('feedbacks')
        cls.client.close()

    def setUp(self):
        self.collection.delete_many({})

    def test_get_all_feedbacks(self):
        # Insert some feedbacks into the collection
        feedbacks = [
            {
                'username': 'user1',
                'user_id': '1',
                'feedback': 'Great app!',
                'date_time': '2022-01-01 10:00:00'
            },
            {
                'username': 'user2',
                'user_id': '2',
                'feedback': 'Awesome!',
                'date_time': '2022-01-02 12:00:00'
            }
        ]
        self.collection.insert_many(feedbacks)

        # Call the function to get all feedbacks
        result = get_all_feedbacks()

        # Check if the result matches the inserted feedbacks
        self.assertEqual(result, feedbacks)

    def test_insert_feedback_existing_user(self):
        # Insert a feedback for an existing user
        existing_user_feedback = {
            'username': 'user1',
            'user_id': '1',
            'feedback': 'Great app!',
            'date_time': '2022-01-01 10:00:00'
        }
        self.collection.insert_one(existing_user_feedback)

        # Call the function to insert a new feedback for the existing user
        new_feedback = {
            'username': 'user1',
            'user_id': '1',
            'feedback': 'Awesome!',
            'date_time': '2022-01-02 12:00:00'
        }
        insert_feedback(new_feedback)

        # Check if the new feedback is added to the existing user's feedbacks
        updated_user_feedback = self.collection.find_one({'user_id': '1'})
        self.assertEqual(len(updated_user_feedback['feedbacks']), 2)
        self.assertEqual(updated_user_feedback['feedbacks'][1]['feedback'], 'Awesome!')

    def test_insert_feedback_new_user(self):
        # Call the function to insert a feedback for a new user
        new_user_feedback = {
            'username': 'user1',
            'user_id': '1',
            'feedback': 'Great app!',
            'date_time': '2022-01-01 10:00:00'
        }
        insert_feedback(new_user_feedback)

        # Check if a new document is inserted for the new user
        inserted_user_feedback = self.collection.find_one({'user_id': '1'})
        self.assertIsNotNone(inserted_user_feedback)
        self.assertEqual(inserted_user_feedback['user_name'], 'user1')
        self.assertEqual(len(inserted_user_feedback['feedbacks']), 1)
        self.assertEqual(inserted_user_feedback['feedbacks'][0]['feedback'], 'Great app!')

if __name__ == '__main__':
    unittest.main()