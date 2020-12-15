Capstone: Casting Agency App
----
## Inspiration :rocket:
My love for rading fantasy stories and Passion for Fullstack development has lead me to this moment as this is my final project for the [Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004). It covers the following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentification with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

----
## Introduction
:book: TellaTale is a community for fictional story lover where they can Read , Write and enjoy each others story tellings. 

* Roles:
    * Reader
        * Can view diffrent Stories & Genres
    * Writer
        * Add ,update and delete Stories owned by them.
    * Admin
        * Add ,update and delete stories owned by writers. 
        * Add ,update and delete storie genres.

## Getting Started

### Dependencies :wrench:

#### Python 3.7

Follow instructions to install the version 3.7.9 of python for your platform on the website  [python](https://www.python.org/downloads/release/python-379/)

#### Virtual Environment
Follow the instruction to create a virtual environment on your machine 
[venv](https://docs.python.org/3/library/venv.html)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the home directory and running:

```bash
pip3 install -r requirements.txt
```

## Project Steps
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the postgres SQL database. You'll primarily work in app.py and can reference models.py. 

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) a flask based extensions that makes it easy to work with SQLALChemy in flask.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Auth0](https://auth0.com/) a platform that simplfies the Authentication & Authorization process , we will be using it along side JWT to build our login system.

## Database Setup
* The database should be named `tellatale`
* The testing database should be named `tellatale_test`

* With Postgres running, import the following tables into the database :
** genre.txt
** stoires.csv

---
**NOTE**

while importing `genre.txt` set the filed to `type` in the table. 

---

## Running the server

From within the `home` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh

flask run --reload
```

---

**NOTE**

before running `source setup.sh` set the *bearer tokens* for both Writer & Admin 

---


## URL

* Heroku: 
* Running locally: http://localhost:5000

## AUTH0 Login Details:
- To generate new Bearer Tokens
* Writer
    * Email:director@capstone.com 
    * Password: Password1!
* Admin
    * Email:producer@capstone.com 
    * Password: Password1!


<!-- ## [Postman](https://getpostman.com) Collections:
- Import the postman collection, navigate to `Postman_tests` directory and select any collections of Postman endpoints tests:
    * `Capstone-Heroku.postman_collection.json`: Heroku endpoints tests with (proper permission) bearer token included
    * `Capstone-Local.postman_collection.json`: Local endpoints tests with (proper permission) bearer token included -->

## API Reference
Getting Started
- Base URL: http://127.0.0.1:5000/

### Endpoints: 

#### GET /stories
- Fetches paginated stories from the database (10 stories per page)
- Request Arguments(optional): ?page=[Page Number]
- Sample: curl http://127.0.0.1:5000/stories
```
{
 "stories": [
     {
      "content": "Was time created or a side effect !?", 
      "cover_image": null, 
      "genre": 1, 
      "genre-name": "Fantasy", 
      "id": 9, 
      "read_time": 1, 
      "release_date": "Wed, 23 Dec 2020 04:05:06 GMT", 
      "released": true, 
      "title": "The machine that made time"
    }, 
    {
      "content": "should the be ranked by chance or glance?", 
      "cover_image": null, 
      "genre": 1, 
      "genre-name": "Fantasy", 
      "id": 10, 
      "read_time": 5, 
      "release_date": "Wed, 23 Dec 2020 04:05:06 GMT", 
      "released": true, 
      "title": "the 5th Rank of wizard"
    }, 
    {
      "content": "should the be ranked by chance or glance?", 
      "cover_image": null, 
      "genre": 3, 
      "genre-name": "Fantasy-Children's Story", 
      "id": 13, 
      "read_time": 5, 
      "release_date": "Wed, 23 Dec 2020 04:05:06 GMT", 
      "released": true, 
      "title": "the 6th Rank of wizard"
    }, 
    {
      "content": "should the be ranked by chance or glance?", 
      "cover_image": null, 
      "genre": 144, 
      "genre-name": "Western-Young Adult", 
      "id": 14, 
      "read_time": 5, 
      "release_date": "Wed, 23 Dec 2020 04:05:06 GMT", 
      "released": true, 
      "title": "the 6th Rank of wizard"
    }
 ],
 "success": true, 
 "total_stories": 10
}
```
#### GET /stories/{story_id}
- Fetch details of provided story_id from database
##### Input:
```
GET http://127.0.0.1:5000/stories/3
```
##### Output:
```
{
  "story": {
    "content": "coming soon 2...", 
    "cover_image": null, 
    "genre": 1, 
    "genre-name": "Fantasy", 
    "id": 3, 
    "read_time": 3, 
    "release_date": "Tue, 08 Dec 2020 04:05:06 GMT", 
    "released": false, 
    "title": "the next big thing"
  }, 
  "success": true
}
```


#### PATCH stories/update/{story_id}
- Update details of a story. This endpoint takes title,
content,cover_image,genre,read_time,released. 
- Returns: multiple key/value pairs object with the following content: 
    * success: True or False 
    * Story: details 

##### Input:
```
curl http://127.0.0.1:5000/stories/update/3 -X PATCH 
{
  "title": "From the sky they came...",
  "content": "coming soon..."
}
```
##### Output:   
```
{
    "story": [
        {
            "content": "coming soon...",
            "cover_image": null,
            "genre": 3,
            "id": 3,
            "read_time": 3,
            "release_date": "Tue, 08 Dec 2020 04:05:06 GMT",
            "released": false,
            "title": "From the sky they came..."
        }
    ],
    "success": true
}
```

#### POST /stories/add
- Creates a new story with the title,cover art , content,read time, released status , release date, genre.  

##### Input:
```
curl http://127.0.0.1:5000/stories/add -X POST -H "Content-Type: application/json" -d   
{
            "content": "should the be ranked by chance or glance?",
            "cover_image": null,
            "genre": 144,
            "read_time": 5,
            "release_date": "Wed, 23 Dec 2020 04:05:06 GMT",
            "released": true,
            "title": "the 6th Rank of wizard"
      }
```
##### Output:
```
{
    "message": "Your story has been Created",
    "success": true
}
```

#### DELETE /stories/delete/{story_id}
- Delete a story with story_id if it exists. 

##### Input:
```
curl -X DELETE http://127.0.0.1:5000/stories/delete/5
```
##### Output:
```
{
    "story_id": 5,
    "success": true
}
```
#### POST /stories/search
- Seacrh stories with title or content phrase. 

##### Input:
```
curl -X DELETE http://127.0.0.1:5000/stories/search
"Content-Type: application/json" -d   
{
        "searcterm: "wizard"
      }
```
##### Output:
```
{
    "stories": [
        {
            "content": "should the be ranked by chance or glance?",
            "cover_image": null,
            "genre": 144,
            "id": 15,
            "read_time": 5,
            "release_date": "Wed, 23 Dec 2020 04:05:06 GMT",
            "released": true,
            "title": "the 6th Rank of wizard"
        }
    ],
    "success": true,
    "total_stories": 1
}
```


#### GET /genres
- Fetches all genres from the database
##### Input
```
curl http://127.0.0.1:5000/genres
```

##### Output
```
{
    "genres": [
        {
            "id": 2,
            "type": "Fantasy-Alternate History"
        },
        {
            "id": 3,
            "type": "Fantasy-Children's Story"
        },
        {
            "id": 4,
            "type": "Fantasy-Comedy"
        }...
    ],
    "success": true,
    "total_genres": 145
}

```

#### GET /genres/{genre_id}/stories
- This endpoint retrieves all stories in a specific genre 
##### Input: 
```
curl 127.0.0.1:5000/genres/1/stories
```
##### Output
```
{
    "current_genre": "Fantasy",
    "stories": [
        {
            "content": "coming soon 2...",
            "cover_image": null,
            "genre": 1,
            "id": 4,
            "read_time": 3,
            "release_date": "Tue, 08 Dec 2020 04:05:06 GMT",
            "released": false,
            "title": "the next big thing"
        },
        {
            "content": "Was time created or a side effect !?",
            "cover_image": null,
            "genre": 1,
            "id": 9,
            "read_time": 1,
            "release_date": "Wed, 23 Dec 2020 04:05:06 GMT",
            "released": true,
            "title": "The machine that made time"
        },
        {
            "content": "should the be ranked by chance or glance?",
            "cover_image": null,
            "genre": 1,
            "id": 10,
            "read_time": 5,
            "release_date": "Wed, 23 Dec 2020 04:05:06 GMT",
            "released": true,
            "title": "the 5th Rank of wizard"
        }
    ],
    "success": true,
    "total_stories": 3
}
```

#### PATCH /genres/update/{genre_id}
- This endpoint should take genre type.
##### Input: 
```
curl http://127.0.0.1:5000/genres/update -X PATCH 
{
    "genre":"Fantasy"
}
```
##### Output
```
{
    "genre": "Fantasy",
    "success": true
}
```

#### POST /genres/add
- This endpoint should take genre type 
- The genre type will be checked for duplicates
##### Input: 
```
curl http://127.0.0.1:5000/genres/add -X POST 
{
    "type":"Fantasy"
}
```
##### Output
```
{
    "message": "New genre has been Created",
    "success": true
}

```
#### DELETE /genres/delete/{genre_id}
- Deleting a genre by its id from the database 

##### Input:
```
curl -X DELETE http://127.0.0.1:5000/genres/delete/155
```
##### Output:
```
{
    "message": "Deleted",
    "success": true
}
```

### Error Handling
```
Errors are returned as JSON objects in the following format:
{   
    "success": False, 
    "error": 422, 
    "message": "Unprocessable"
}
```
The API will return five error types when requests fail: 
- 404: Resource Not Found
- 422: Not Processable
- 401: Unauthorized
- 403: Access to the requested resource is forbidden
- 500: Internal Server Error
- Authorization errors:
-- Invalid Claims.
-- Unauthorized.
-- Token expired.
-- Unable to parse authentication token.
-- Unable to find the appropriate key.