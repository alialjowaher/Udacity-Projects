# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.


# API 
* All Responses are in JSON format including Errors.
## Endpoints

```

List of Endpoints:

GET '/categories'
GET '/questions'
GET '/categories/<int:id>/questions'

POST **'/questions/add'
POST **'/questions/search'
POST **'/quizzes'**

DELETE 'questions/<int:question_id>'

```

### GET **'/categories'**

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

* **Categories Attributes** 
    - id
    - type

- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

curl http://127.0.0.1:5000/categories

**Response:** 
```
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}

```


### GET **'/questions'**

- Fetches a dictionary of **10 questions**  per **page** in which the keys are the ids.

* **Questions Attributes**
    - id 
    - question 
    - answer 
    - category 
    - difficulty

- Request Arguments: '?page=' (by default page 1 is returnd)
- Catgories list as key:value is returned befor the questions dictonary.
- **Total Questions** and **success** variables are returned after the questions dictonary.
- Returns: A  dictionary of objects with a  key, questions, answer, category , difficulty as key:value pairs.

curl http://127.0.0.1:5000/questions

**Response:** 
```
{
  "categories": {
    "1": "science",
    ... Omitted for bravery
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
   ... Omitted for bravery
  ],
  "success": true,
  "total_questions": 19
}

```

### GET **'/categories/<int:id>/questions'**

- Fetches a dictionary of **10 questions** per **page** for a specific **category**.

* **Questions for Category Attributes**
    - id 
    - question 
    - answer 
    - category 
    - difficulty

- Request Arguments: '<int:id>' (**required**) represents a category code 
- current category as key:value is returned befor the Questions for Category dictonary.
- **Total Questions** and **success** variables are returned after the dictonary.
- Returns: A  dictionary of objects with a  key, questions, answer, category , difficulty as key:value pairs.

curl http://127.0.0.1:5000/categories/<int:id>/questions

**Response:** 
```
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    ... Omitted for bravery
  ],
  "success": true,
  "total_questions": 3
}
```

### POST **'/questions/add'**

- Create a Question in a specific category.

* **Add a Question Attributes**
    
    - question (required) 
    - answer  (required)
    - category (required)
    - difficulty (required)

- Request Arguments: All Attributes are required. 
- Returns: an object with  key:value pairs , includes success and message variable.

curl -X POST http://127.0.0.1:5000//questions/add

**Response:** 
```

{
    'success': True,
    'message': 'The Question has been added Successfully !',
 }

```

### DELETE **'/questions/<int:question_id>'**

- Delete a specific question using the Question ID.

* **DELETE a Question Attributes**
    
    - id (required) 
    
- Request Arguments: id . 
- Returns: an object with  key:value pairs , includes success and question id variable.

curl -X DELETE http://127.0.0.1:5000/questions/<int:questions_id>

**Response:** 
```

{
   'success': True,
   'question_id': question_id,
 }

```

### POST **'/questions/search'**

- Search using questions titles .
- Return partail matchs.

* **Search Questions Attributes**
    
    - searchTerm (required)
    
- Request Arguments: searchTerm . 
- Returns: an object with  key:value pairs , includes matching questions, success and 
total questions variables.

curl -X POST http://127.0.0.1:5000/questions/search>

**Response:** 
```
{
   'success': True,
   'questions': current_questions,
   'total_questions': len(search_questions),
}

```


### POST **'/quizzes'**

- Play the quiz game 
- Returns a collection of 5 questions.
- If no category is provided a random question will be picked.
- ** If the category has less than 5 questions , random questions from other categories will
be added picked up to a total of 5.

* **Quiz Game Attributes**
    
    - category (optional)
    
- Request Arguments: None . 
- Returns: an object with  key:value pairs , includes next questions and success variables.


curl -X POST http://127.0.0.1:5000/quizzes>

**Response:** 
```
{
    'success': True,
    'question': next_question.format()
}

```

## HTTP error messages 

* This section cover the HTTP Errors and responses description.


### Error Code : **400** 

- Description : **BAD REQUEST** , the sumbitted data contained invalid values.

``` 
{
    'success': False,
    'error': 400,
    'message': 'A Bad Request'
} 

```

### Error Code : **404** 

- Description : **NOT FOUND** , the requested resource can't be located.

``` 
{
    'success': False,
    'error': 404,
    'message': 'The Resource Was Not Found'
}

```

### Error Code : **405** 

- Description : **METHOD NOT ALLOWED** , the requested method is known by the server but is not supported by the resource.

``` 
{
    'success': False,
    'error': 405,
    'message': 'The Method is Not Allowed'
}

```
### Error Code : **422** 

- Description : **UNPROCESSABLE ENTITY** , the server can understand the request content type and syntax is correct but was unable to process the contained insturctions .

``` 
{
    'success': False,
    'error': 422,
    'message': 'Unprocessable Entity'
}

```

### Error Code : **500** 

- Description : **INTERNAL SERVER ERROR ** , the server encountred an unexpected condition which prevented it from completing the request (generic / catch-all error type) .

``` 
{
    'success': False,
    'error': 500,
    'message': 'Internal Server Error'
}

```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
