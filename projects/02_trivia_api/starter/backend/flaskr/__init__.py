import os
from os import sep
from random import choice
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
        categories = {}

        # @Done: return 404 formated error
        if all_categories is None:
            abort(404)
        else:

            for category in all_categories:

                categories[category.id] = category.type.lower()

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
  ten questions per page and pagination at the bottom of the screen for three
  pages.
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

        # @Done: return 404 formated error
        if len(current_questions) == 0:
            abort(404)
        else:
            all_categories = Category.query.order_by(Category.id).all()
            categories = {}
            for category in all_categories:
                # categories.append(category.type.lower())
                categories[category.id] = category.type.lower()

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(all_questions),
                'categories': categories,

            })

    '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be
  removed.
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

        except Exception:
            abort(422)

        '''
  @Done:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions/add', methods=['POST'])
    def create_question():

        content = request.get_json()
        question = content.get('question')
        answer = content.get('answer')
        difficulty = content.get('difficulty')
        category = content.get('category')

        if not question or not answer or not difficulty or not category:
            abort(422)

        try:
            new_question = Question(question=question, answer=answer,
                                    difficulty=difficulty, category=category)
            new_question.insert()

            return jsonify({
                'success': True,
                'message': 'The Question has been added Successfully !',
            })
        except Exception:
            abort(422)

    '''
  @Done:
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
        search_term = search.get('searchTerm', '')

        try:
            search_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            current_questions = pagination(request, search_questions)
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(search_questions),
            })
        except Exception:
            abort(404)

    '''
  @Done:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_in_categories(id):
        category = Category.query.get(id)

        if(category is None):
            abort(422)

        filtered_questions = Question.query.filter_by(category=id).all()
        questions_in_category = pagination(request, filtered_questions)

        return jsonify({
            'success': True,
            'questions': questions_in_category,
            'total_questions': len(filtered_questions),
            'current_category': category.type

        })
    '''
  @Done:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz_game():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        category = data.get('quiz_category')

        if(category is None) or (previous_questions is None):
            abort(400)

        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(
                category=category['id']).all()

        def get_random_question():
            # https://realpython.com/list-comprehension-python/

            category_used_questions = [
                question for question in questions if question.id not
                in previous_questions]
            all_questions = Question.query.all()
            all_categoryies = [
                question for question in all_questions if question.id not
                in previous_questions]
            '''
             if the current category reaches 0 questions , add extra random 
             questions from other categories 
            '''
            if (len(category_used_questions) == 0):
                random_questions = random.choice(all_categoryies)
            else:
                random_questions = random.choice(category_used_questions)

            return random_questions

        next_question = get_random_question()

        return jsonify({
            'success': True,
            'question': next_question.format()
        })

    '''
  @Done:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'A Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'The Resource Was Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'The Method is Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
