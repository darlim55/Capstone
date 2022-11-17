import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db,Movie, Actor
from flask_migrate import Migrate
# from dotenv import load_dotenv

# load_dotenv()

class Testcaseagencyapp(unittest.TestCase):


    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgres://{}/{}".format('localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

        DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
   
        self.director = {
            "Authorization": "Bearer {}".format(DIRECTOR_TOKEN) }

        self.actor = {
            "name": "Jorge Darlim",
            "age": 28,
            'gender': 'masculino',
            'id': 6
        }

        self.add_actor = {
            "name": "Kit Harington",
            "age": 33,
            'gender': 'masculino',
            'id': 7
        }


        self.movie = {
            'title': "harry potter",
            'release_date': "2000-05-06 00:00:00",
            'id': 6
        }

        self.add_movie = {
            'title': "Percy Jackson",
            'release_date': "2012-05-02 00:00:00",
            'id': 7,
        }

        self.update_movie = {
            'title': "Honest Thief",
            'release_date': "2016-02-04 00:00:00",
            'id': 7
        }


    def tearDown(self):
        """Executed after reach test"""
        pass

    def home(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["condition"])

    def test_actor_invalid_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

   
    def test_movies_invalid_token(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
    def test_movies(self):
        res = self.client().get('/movies', headers=self.director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

'''  def test_actor(self):
        print(self.director_header)
        res = self.client().get('/actors', headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
''' 


''' 
    # Tests for castins_director (POST/DELETE/PATCH)
    def test_post_actors(self):
        res = self.client().post('/actors', json=self.add_actor,
                                 headers=self.director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors(self):
        res = self.client().patch('actors/7', json=self.update_actor,
                                  headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_500_patch_actors(self):
        res = self.client().patch('actors/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_post_error_401_actor(self):
        res = self.client().post('/actors', json=self.add_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors(self):
        res = self.client().delete('actors/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


    def test_director_500_patch_movies(self):
        res = self.client().patch('movies/1', headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_patch_movie(self):
        res = self.client().patch('movies/7', json=self.update_movie,
                                  headers=self.director_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

   '''
# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()