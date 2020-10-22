import os
from flask import Flask, request, abort, jsonify, redirect
from flask.helpers import url_for
from sqlalchemy.sql.base import NO_ARG
from werkzeug import datastructures
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route
  after completing the TODOs
  '''
    CORS(app)
   # cors = CORS(app, resources={r"*": {"origins": "*"}})
    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        all_categories = Category.query.order_by(Category.id).all()
        categories = []

        # @TODO: return 404 formated error
        if all_categories is None:
            abort(404)
        else:

            for category in all_categories:
                categories.append(category.type)

            return jsonify({
                'success': True,
                'categories': categories
            })

    '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    def pagination(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = pagination(request, all_questions)

        # @TODO: return 404 formated error
        if len(current_questions) == 0:
            abort(404)
        else:
            all_categories = Category.query.order_by(Category.id).all()
            categories = []
            for category in all_categories:
                categories.append(category.type.lower())

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(all_questions),
                'categories': categories,

            })

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        try:
            question.delete()
            # front-end handles redirect on success message
            return jsonify({
                'success': True,
                'question_id': question_id,
            })

        except:
            abort(422)

        '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
    
                  content = request.get_json()
                  question = content.get('question')
                  answer = content.get('answer')
                  difficulty = content.get('difficulty')
                  category = content.get('category')
                  
                  
                  if not question or not answer or not difficulty or not category:
                      abort(422)  
                  
                  try:
                      new_question = Question(question=question,answer=answer,
                      difficulty=difficulty,category=category)
                      new_question.insert()
                      all_questions = Question.query.order_by(Question.id).all()
                      current_questions = pagination(request, all_questions)
                  

                      return jsonify({
                        'success': True,
                        'message':'The Question has been added Successfully !',
                      })
                  except Exception:
                      abort(422)
                  


    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search = request.get_json()
        search_term = search.get('searchTerm','')
        print(search)
        print(search_term)
        try:
            search_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = pagination(request, search_questions)
            return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(search_questions)
            })
        except:
          abort(404)
    
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
