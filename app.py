import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor

'''from auth.auth import AuthError, requires_auth'''

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


    '''@requires_auth('view:movies')'''
    @app.route('/movies', methods=['GET'])
    def retrieve_movies():
        movies = Movie.query.all()
        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies]
        })


    '''@requires_auth('view:actors')'''
    @app.route('/actors', methods=['GET'])
    def retrieve_actors():
        actors = Actor.query.all()
        return jsonify({
            "success": True,
            "actors": [actor.format() for actor in actors]
        })
        
        
        
    '''@requires_auth('post:movies')   '''
    @app.route('/movies', methods=['POST'])
    def create_movie():
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



    '''@requires_auth('post:actors')'''
    @app.route('/actors', methods=['POST'])
    def create_actor():
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

   
    
    '''@requires_auth('delete:movies')'''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404, "No movie with given id " + str(movie_id) + " is found")

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })


    
    '''@requires_auth('delete:actors')    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404, "No actor with given id " + str(actor_id) + " is found")

        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })


    '''@requires_auth('update:movies') '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):

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
    def update_actor(actor_id):

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

    '''@app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error['description']
        }), auth_error.status_code'''

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)