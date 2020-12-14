import os , datetime
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy.orm import backref

database_name = "tellatale"
database_path = "postgres://{}/{}".format(
    'postgres:alinet20@localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Story(db.Model):
    __tablename__ = "stories"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    cover_image = db.Column(db.String())
    genre = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.Text())
    release_status = db.Column(db.Boolean, default=False)
    release_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    read_time = db.Column(db.Integer())
    Author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    def cover(self):
        return {
            'title': self.title,
            'cover_art': self.cover_image,
            'read-time': self.read_time
        }
    
    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'cover_image': self.cover_image,
            'genre': self.genre,
            'content': self.content,
            'release_date': self.release_date,
            'released': self.release_status,
            'read_time': self.read_time,
            
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), nullable=False) #roels : Author , Admin
    #TODO should we delete all stories owned by User when his account is deleted?!
    stories = db.relationship('Story', backref='users',lazy=True)

    def userInfo(self):
        return{
            'role':self.role,
            'stories':self.stories
        }


class Genre(db.Model):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
        
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
# class Reactions(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     story_id = db.Column(db.Integer, db.ForeignKey("story.id"), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     emoji_text = db.Column(db.ARRAY(db.String()), nullable=False)


