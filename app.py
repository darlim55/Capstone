import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
import psycopg2
from auth import AuthError, requires_auth

from datetime import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response



    @app.route('/')
    def get_greeting():
        greeting = "Welcome to Agency! You can get JWT here." 
        return greeting
    
    @app.route('/movie', methods=['GET'])
    @requires_auth('get:movie')
    def retrieve_movies(payload):
        movies = Movie.query.all()
        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]
        })
     

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(payload):
    
        actors = Actor.query.all()
        return jsonify({
            "success": True,
            "actors": [actor.format() for actor in actors]
        })
       

        
        
    '''@requires_auth('post:movies')   '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post: movies')
    def create_movie(jwt):
        body = request.get_json()

        if body is None:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None or release_date is None:
            abort(400, "Missing field for Movie")

        movie = Movie(title=title,
                      release_date=release_date)

        movie.insert()

        return jsonify({
            "success": True
        })


    @app.route('/actors', methods=['POST'])
    @requires_auth('post: actors')
    def create_actor(jwt):
        body = request.get_json()

        if body is None:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        if name is None or age is None or gender is None or movie_id is None:
            abort(400, "Missing field for Actor")

        if  Movie.query.filter_by(id=movie_id).first():
            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        

            actor.insert()

            return jsonify({
                "success": True
            })
        else:
             abort(404, "No movie with given id " + str(movie_id) + " is found")

   
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt,movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404, "No movie with given id " + str(movie_id) + " is found")

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })


    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete: actors')
    def delete_actor(jwt,actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404, "No actor with given id " + str(actor_id) + " is found")

        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt,movie_id):

        updated_movie = Movie.query.get(movie_id)

        if not updated_movie:
            abort(
                404,
                'Movie with id: ' + str(movie_id) + ' could not be found.')

        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None or release_date is None:
                    abort(400, "Missing field for Actor")

       
        updated_movie.title = title
        updated_movie.release_date = release_date

        updated_movie.update()

        return jsonify({
            "success": True,
            "updated": updated_movie.format()
        })

 
    '''@requires_auth('update:actors')'''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt,actor_id):

        updated_actor = Actor.query.get(actor_id)

        if not updated_actor:
            abort(
                404,
                'Actor with id: ' +
                str(actor_id) +
                ' could not be found.')

        body = request.get_json()


        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)
        if name is None or age is None or gender is None or movie_id is None:
            abort(400, "Missing field for Actor")
            
        if  Movie.query.filter_by(id=movie_id).first():
 
            updated_actor.name = name
            updated_actor.age = age
            updated_actor.gender = gender
            updated_actor.movie_id = movie_id

            updated_actor.update()
      

            return jsonify({
                "success": True,
                "updated": updated_actor.format()
            })
        else:
            abort(404, "No movie with given id " + str(movie_id) + " is found")
            

    def get_error_message(error, default_message):
        try:
            return error.description
        except BaseException:
            return default_message

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": get_error_message(error, "unprocessable"),
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": get_error_message(error, "resource not found")
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": get_error_message(error, "bad request")
        }), 400
        
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8100, debug=True)