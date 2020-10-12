from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_migrate import Migrate
from datetime import datetime
import dateutil.parser
# app = Flask(__name__)


# app.config.from_object("config")

db = SQLAlchemy()

# TODO: connect to a local postgresql database



# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    website = db.Column(db.String())
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    is_seeking_talent = db.Column(db.Boolean, default=True)
    seeking_talent_messge = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    shows = db.relationship("Show", backref="Venue", lazy="dynamic" ,)  # lazy = True or lazy=dynamic which works better in our case !?
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    # Relationship with Shows (Show_id)


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String(500))
    is_seeking_venue = db.Column(db.Boolean, default=True)
    seeking_venue_messge = db.Column(db.String())
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    shows = db.relationship("Show", backref="Artist", lazy=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = "shows"

    id = id = db.Column(db.Integer(), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now)


# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_many_to_many_relationships.htm

