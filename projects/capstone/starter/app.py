import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Genre, Story , User, setup_db 
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  
  setup_db(app)

  CORS(app)

  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response


  
  
  
  STORY_PER_PAGE = 10

  #Done pagination helper
  def pagination(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * STORY_PER_PAGE
        end = start + STORY_PER_PAGE
        stories = [story.details() for story in selection]
        current_stories = stories[start:end]
        return current_stories

  #Done Get all stories
  @app.route('/stories', methods=['GET'])
  def get_stories():
    
    all_stories = Story.query.all()
    current_stories = pagination(request,all_stories)     
    
    if len(current_stories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'stories': current_stories,
      'total_stories': len(all_stories)
    }), 200
  #Done Add new story
  @app.route('/stories/add', methods=['POST'])
  def create_story():
    form = request.get_json()
    
    title = form.get('title')
    cover_image= form.get('cover_image')
    genre = form.get('genre')
    content= form.get('content')
    release_date = form.get('release_date')
    release_status = form.get('released')
    read_time = form.get('read_time')

    if not title or not content or not genre or not release_date or not release_status:
      abort(422)
    
    try:
      new_story = Story(title=title,cover_image=cover_image,genre=genre,content=content,release_date=release_date,
                        release_status=release_status,read_time=read_time)
      new_story.insert()
      
      return jsonify({
        'success': True,
        'message':'Your story has been Created'
        # 'story_id':
      }),201

    except Exception as e:
      print(e)
      abort(422)
  #TODO Update , Delete , Search
    
  @app.route('/genres', methods=['GET'])
  def get_genres():
    all_genres = Genre.query.all()
    genres = {}
# [genre.format() for genre in all_genres]
    for genre in all_genres:
      genres[genre.id] = genre.type

    return jsonify({
      'success': True,
      'genres': genres,
      'total_genres':len(genres)
    }),200
  

  @app.route('/genres/<int:id>/stories', methods=['GET'])
  def get_stories_in_genres(id):
    genre = Genre.query.get(id)
    
    if(genre is None):
      abort(422)
  
    filtred_genre = Genre.query.filter_by(genre=id).all()
    stories_in_genre = pagination(request, filtred_genre)

    return jsonify({
      'success':True,
      'stories': stories_in_genre,
      'total_stories':len(filtred_genre),
      'current_genre': genre.type
    }),200


  return app

APP = create_app()



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)