import os
from sqlalchemy import Column, String, Integer, create_engine, sql
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "stories"
database_path = "postgres://{}/{}".format(
    'postgres:postgres@localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Story(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    cover = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    content = db.Column(db.Text())
    release_status = db.Column(db.Boolean, default=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read_time = db.Column(db.Integer())


# CRUD operations abstract
class User(db.Model):
    
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)


#TODO complete classes & endpoints 