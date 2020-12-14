
import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from app import create_app
from models import setup_db, Story , Genre


#tokens for testing 
WRITER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1jek5qNktlbUF1d0FPWTR5aU0tSSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWxpai51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTczNjIwMzcxOTkyOTk0NjkwMzYiLCJhdWQiOlsidGVsbGF0YWxlIiwiaHR0cHM6Ly9mc25kLWFsaWoudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwNzkyNTczNiwiZXhwIjoxNjA3OTMyOTM2LCJhenAiOiI3NndhempKNlBVa0ZCUzRvazRwOWxEN3k5T2tTWUlZQyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6c3RvcnkiLCJkZWxldGU6c3RvcnkiLCJ1cGRhdGU6c3RvcnkiXX0.mBti8g5TiCTPBWfm5vQYMYjddQkg0Zf93RTfis7bNYfB3oCJKWUevvIEjY3Dh6dttA1LTXWIjn4lEReu8fcUBzzEGAJMf-Pku1SAo-aAVmFFC457qqhm8dF-kkE1JUyYJQcxjFdOSX6BGTuijdTbbZxiMZwAiumZBDwgwYO9130CVRLvKb443a00bPG9azkH3mE3VmvwGB9S4HjySgBuecmpG-i36-24adFOLLLY5beaMy-drR81ybJYSw_rdVq_6bcsYL660ytPQd9S1_zkn2jTnrW4AwC2gXrk_S4Fd4Js5sh-atap0ITac1SNBc-U65MxIuTit1_-XBiY4W3D1g'
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
    
    """ Stories endpoint tests """

    # Paginated Stories
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
    def test_create_story_success(self):
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

    def test_update_story_success(self):
        res = self.client().patch('/stories/update/22',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'title':'updated title','cover_image':'test image link',
        'genre':'1','content':'test content of a story',
        'release_date':'2020-12-08 04:05:06','released':True,'read-time':3 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
    
    def test_update_story_fail(self):
        res = self.client().patch('/stories/update/40000',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'title':'updated title'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'], False)
    

    def test_delete_story(self):
        res = self.client().delete('/stories/delete/36',headers={'Authorization': 'Bearer '+ WRITER_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['story_id'], 36)
    
    def test_delete_story_fail(self):
        res = self.client().delete('/stories/delete/40000',headers={'Authorization': 'Bearer '+ WRITER_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'], False)
        
    
    """ Genres endpoint tests  ONLY ADMIN CAN PERFORM CRUD OPERATIONS ON GENRES """

    def test_get_genres_list(self):
       res = self.client().get('/genres')
       data = json.loads(res.data)
       self.assertEqual(res.status_code, 200)
       self.assertTrue(data['success'], True)
       self.assertTrue(data['genres'])
       self.assertTrue(data['total_genres'])

    def test_get_story_in_genre(self):
       res = self.client().get('/genres/1/stories')
       data = json.loads(res.data)
       self.assertEqual(res.status_code, 200)
       self.assertTrue(data['success'], True)
       self.assertTrue(data['stories'])
       self.assertTrue(data['total_stories'])
       self.assertTrue(data['current_genre'])
 
    def test_create_genre(self):
      res = self.client().post('/genres/add',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'type':'Fake'})
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 201)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['message'], 'New genre has been Created')

    def test_update_genre(self):
      res = self.client().patch('/genres/update/1',headers={'Authorization': 'Bearer '+ WRITER_TOKEN},
        json={'genre':'fantasy'})
      data = json.loads(res.data)
      self.assertEqual(res.status_code,200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['genre'])

    def test_delete_genre(self):
      res = self.client().delete('/genres/delete/145',headers={'Authorization': 'Bearer '+ WRITER_TOKEN})
      data = json.loads(res.data)
      self.assertEqual(res.status_code,422)
      self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()