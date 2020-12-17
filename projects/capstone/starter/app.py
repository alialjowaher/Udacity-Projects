import json
import os
from re import split
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.log import Identified
from sqlalchemy.util.langhelpers import generic_repr
from models import Genre, Story, User, setup_db
from auth import AuthError, requires_auth
from flask_migrate import Migrate


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    CORS(app)
    STORY_PER_PAGE = 10

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Done pagination helper
    def pagination(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * STORY_PER_PAGE
        end = start + STORY_PER_PAGE
        stories = [story.details() for story in selection]
        current_stories = stories[start:end]
        return current_stories

    # Done Get all stories
    @app.route('/stories', methods=['GET'])
    def get_stories():
        # return released stories
        all_stories = Story.query.filter_by(release_status='true').all()
        current_stories = pagination(request, all_stories)
        # append story-type to story
        for story in current_stories:
            get_author_name = User.query.get(story['author_id'])
            story['author_name'] = get_author_name.name
            get_genre_type = Genre.query.get(story['genre'])
            story['genre_name'] = get_genre_type.type

        if len(current_stories) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'stories': current_stories,
          'total_stories': len(all_stories)
        }), 200

    # Done Add new story
    @app.route('/stories/add', methods=['POST'])
    @requires_auth('create:story')
    def create_story(payload):
        data = request.get_json()
        # DONE: get user e-mail from JWT token & allow only owner to edit post
        # https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
        get_email = json.dumps(payload['https://tellatale.com/email'])
        email = (get_email.split('"')[1].split('"')[0])
        user_exists = User.query.filter_by(email=email).first()
        if not user_exists:
            temp_name = (email.split("@")[0])
            new_user = User(email=email, name=temp_name)
            new_user.insert()
            author_id = new_user.id
        else:
            author_id = user_exists.id

        title = data.get('title')
        cover_image = data.get('cover_image')
        genre = data.get('genre')
        content = data.get('content')
        release_date = data.get('release_date')
        release_status = data.get('released')
        read_time = data.get('read_time')

        if (not title or not content or not genre
           or not release_date or not release_status):
            abort(422)

        try:
            new_story = Story(title=title, cover_image=cover_image,
                              genre=genre, content=content,
                              release_date=release_date,
                              release_status=release_status,
                              read_time=read_time,
                              author_id=author_id)
            new_story.insert()

            return jsonify({
              'success': True,
              'message': 'Your story has been Created'
            }), 201

        except Exception:
            abort(422)

    # Done get a single story by id
    @app.route('/stories/<int:story_id>', methods=['GET'])
    def get_story(story_id):

        story = Story.query.get(story_id)
        # get genre type as name in story
        genre_type = Genre.query.get(story.genre)
        get_author_name = User.query.get(story.author_id)
        if story is None:
            abort(404)

        story = story.details()
        story["genre_name"] = genre_type.type
        story['author_name'] = get_author_name.name

        return jsonify({
          'success': True,
          'story': story,
        }), 200

    # Done Delete a story
    @app.route('/stories/delete/<int:story_id>', methods=['DELETE'])
    @requires_auth('delete:story')
    def delete_story(payload, story_id):
        story = Story.query.get(story_id)
        if story == 0:
            abort(404)  
        try:
            story.delete()
            return jsonify({
              'success': True,
              'story_id': story_id
            }), 200
        except Exception:
            abort(422)

    # Done Update story content
    @app.route('/stories/update/<int:story_id>', methods=['PATCH'])
    @requires_auth('update:story')
    def update_story(payload, story_id):

        data = request.get_json()
        story = Story.query.get(story_id)
        # check if your the owner of the story to update it.
        get_email = json.dumps(payload['https://tellatale.com/email'])
        email = (get_email.split('"')[1].split('"')[0])
        story_owner = User.query.get(story.author_id)

        if story is None:
            abort(404)
        if story_owner.email != email:
            abort(401)
        try:
            title = data.get('title')
            cover_image = data.get('cover_image')
            genre = data.get('genre')
            content = data.get('content')
            release_date = data.get('release_date')
            release_status = data.get('released')
            read_time = data.get('read_time')

            if title:
                story.title = title
            if cover_image:
                story.cover_image = cover_image
            if genre:
                story.genre = genre
            if content:
                story.content = content
            if release_date:
                story.release_date = release_date
            if release_status:
                story.release_status = release_status
            if read_time:
                story.read_time = read_time

            story.update()

            return jsonify({
              'success': True,
              'story': [story.details()]
            }), 200

        except Exception:
            abort(422)

    # Basic search by title or content and retrun released stories only
    @app.route('/stories/search', methods=['POST'])
    def search_question():
        search = request.get_json()
        search_term = search.get('searchterm', '')
        try:
            search_stories = Story.query.filter(
                Story.title.ilike(f'%{search_term}%') |
                Story.content.ilike(f'%{search_term}%') &
                Story.release_status == 'true').all()
            current_stories = pagination(request, search_stories)
            return jsonify({
                   'success': True,
                   'stories': current_stories,
                   'total_stories': len(search_stories),
            })
        except Exception:
            abort(404)

    # Done all genres list
    @app.route('/genres', methods=['GET'])
    def get_genres():
        all_genres = Genre.query.all()
        genres = [genre.format() for genre in all_genres]
        return jsonify({
          'success': True,
          'genres': genres,
          'total_genres': len(genres)
        }), 200

    # Done add new genre
    @app.route('/genres/add', methods=['POST'])
    @requires_auth('create:genre')
    def create_genre(payload):
        data = request.get_json()
        type = data.get('type')
        if not type:
            abort(422)
        # prevent duplicate genres
        exists = Genre.query.filter_by(type=type).all()
        # what would be sutable HTTP error code !
        if exists:
            return jsonify({
              'success': False,
              'message': 'Genre already exists'
            })

        try:
            new_genre = Genre(type=type)
            new_genre.insert()
            return jsonify({
              'success': True,
              'message': 'New genre has been Created'
            }), 200
        except Exception:
            abort(422)

    # Done Delete a genre
    @app.route('/genres/delete/<int:genre_id>', methods=['DELETE'])
    @requires_auth('delete:genre')
    def delete_genre(payload, genre_id):
        genre = Genre.query.get(genre_id)
        if genre is None:
            abort(404)

        try:
            genre.delete()

            return jsonify({
              'success': True,
              'message': 'Deleted'
            })

        except Exception:
            abort(422)

    # Done Update genre type
    @app.route('/genres/update/<int:genre_id>', methods=['PATCH'])
    @requires_auth('update:genre')
    def update_genre(payload, genre_id):
        data = request.get_json()
        try:
            genre = Genre.query.get(genre_id)
            if genre is None:
                abort(404)
            genre_to_update = data.get('genre')
            if genre:
                genre.type = genre_to_update
            genre.update()
            return jsonify({
              'success': True,
              'genre': genre.type
            }), 200

        except Exception:
            abort(422)

    # Done get all stories in a genre
    @app.route('/genres/<int:id>/stories', methods=['GET'])
    def get_stories_in_genres(id):
        genre = Genre.query.get(id)
        if(genre is None):
            abort(422)
        stories = Story.query.filter_by(genre=id).all()
        stories_in_genre = pagination(request, stories)
        if len(stories) == 0:
            abort(404)
        return jsonify({
          'success': True,
          'stories': stories_in_genre,
          'total_stories': len(stories),
          'current_genre': genre.type
        }), 200

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(401)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access to the requested resource is forbidden"
        }), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def authntication_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": "Authorization Error"
        }), error.status_code

    return app

    app = create_app()

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
