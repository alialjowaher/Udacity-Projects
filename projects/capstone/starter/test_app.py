
import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from app import create_app
from models import setup_db, Story , Genre


#tokens for testing 
WRITER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1jek5qNktlbUF1d0FPWTR5aU0tSSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWxpai51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTczNjIwMzcxOTkyOTk0NjkwMzYiLCJhdWQiOlsidGVsbGF0YWxlIiwiaHR0cHM6Ly9mc25kLWFsaWoudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwNzg1OTczOSwiZXhwIjoxNjA3ODY2OTM5LCJhenAiOiI3NndhempKNlBVa0ZCUzRvazRwOWxEN3k5T2tTWUlZQyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6c3RvcnkiLCJkZWxldGU6c3RvcnkiLCJ1cGRhdGU6c3RvcnkiXX0.a8Bg679MfYBUeTd__IIVGxDUQ-Qug8r5yiHLCOGn0Uyx7KSno8NeDH6kC7jtLdrF8XEXFpszi4nKVXMKUJ6Ux3X4drlwQc1qVVxft4d_ql4VMuFPGg4jiRXiSOzhrgWI7wTnwRNxZAajaVZmpeu-x8rRZfRAo4LMx0Igho76aI4fx3RHr7n_276yJkDHcHWtE5sKSpZ5d-NWi_eGYI0w3Lj1bzu0RndUscCwjqIYgd-Q8qljY9qBBO6GWcA-fFnELt_SAyjvldi2Ox3azw7ySYgzz9RQyuawJWiARdMOfwTKfrJcwIqdcXEpCQ3KpIV-wdJYM1zdv9VM_DfLwwMhZQ'
ADMIN_TOKEN = ''

class TellaTaleTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "tellatale_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:alinet20@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # Stories endpoint tests

    # {p}aginated Stories
    def test_get_paginated_stories(self):
        res = self.client().get('/stories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['stories'])
        self.assertTrue(data['total_stories'])
    
    # Single Story
    def test_get_story_by_id(self):
        res = self.client().get('/stories/3')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['story'])
        
    # Paginated stories range
    def test_get_paginated_stories_beyond_valid_page(self):
        res = self.client().get('/stories?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # Create a new story [requires JWT] or remove comment out requires Auth in app.py
    def test_create_story(self):
        res = self.client().post('/stories/add',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'title':'test title','cover_image':'test image link',
        'genre':'1','content':'test content of a story',
        'release_date':'2020-12-08 04:05:06','released':True,'read-time':3 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Your story has been Created')


    def test_create_story_fail(self):
        res = self.client().post('/stories/add',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'title':'','cover_image':'test image link','genre':'1',
        'content':'test content of a story',
        'release_date':'2020-12-08 04:05:06','released':True,'read-time':0 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_update_story(self):
        res = self.client().patch('/stories/update/22',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'title':'updated title','cover_image':'test image link',
        'genre':'1','content':'test content of a story',
        'release_date':'2020-12-08 04:05:06','released':True,'read-time':3 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        

    # def test_delete_story(self):
    
    # def test_get_genres_list(self):
    
    # def test_get_story_in_genre(self):
    
    # def test_create_genre(self):
    
    # def test_update_genre(self):

    # def test_delete_genre(self):



if __name__ == "__main__":
    unittest.main()