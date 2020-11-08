import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:alinet20@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_get_catgories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])

    def test_404_get_paginated_question_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The Resource Was Not Found')

    def test_get_questions_based_on_category(self):
        category_id = '1'
        category_type = 'Science'
        res = self.client().get('/categories/'+ category_id +'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'], category_type)

    def test_422_get_questions_based_on_category_does_not_exist(self):
        fake_id = '200'
        res = self.client().get('/categories/'+ fake_id +'/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        
    def test_create_question(self):
        res = self.client().post('/questions/add',json={'question':'test question',
                                                        'answer':'test answer',
                                                        'category':'1','difficulty':'1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Question has been added Successfully !')
    
    def test_422_create_question_failed(self):
        res = self.client().post('/questions/add',json={'question':'',
                                                        'answer':'',
                                                        'category':'1','difficulty':'1'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_delete_question(self):
        question_id = '32'
        res = self.client().delete('questions/'+question_id)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)        
        self.assertEqual(data['question_id'], int(question_id))     
    
    def test_404_delete_question_failed(self):
        question_id = '30000'
        res = self.client().delete('questions/'+question_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'], 'The Resource Was Not Found')    

    def test_quizzes_game(self):
        res = self.client().post('/quizzes',json={'previous_questions': [],
                                                   'quiz_category': 
                                                       {'type': 'sports', 'id': '6'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)         
    
    def test_400_quizzes_game_failed(self):
        res = self.client().post('/quizzes',json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)         
        self.assertEqual(data['message'], 'A Bad Request')


# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
