from datetime import datetime
from enum import Enum
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, AnyOf, Length, URL , Regexp


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class State(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'
    @classmethod
    def choices(selectedState):
        return [(choice.value, choice.name) for choice in selectedState]
class Genres(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    R_and_B = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def choices(selectedGeners):
        return [ (choice.value, choice.value) for choice in selectedGeners ]

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(),AnyOf([ choice.value for choice in State])],
          choices=State.choices()
        # choices=[
        #     ('AL', 'AL'),
        #     ('AK', 'AK'),
        #     ('AZ', 'AZ'),
        #     ('AR', 'AR'),
        #     ('CA', 'CA'),
        #     ('CO', 'CO'),
        #     ('CT', 'CT'),
        #     ('DE', 'DE'),
        #     ('DC', 'DC'),
        #     ('FL', 'FL'),
        #     ('GA', 'GA'),
        #     ('HI', 'HI'),
        #     ('ID', 'ID'),
        #     ('IL', 'IL'),
        #     ('IN', 'IN'),
        #     ('IA', 'IA'),
        #     ('KS', 'KS'),
        #     ('KY', 'KY'),
        #     ('LA', 'LA'),
        #     ('ME', 'ME'),
        #     ('MT', 'MT'),
        #     ('NE', 'NE'),
        #     ('NV', 'NV'),
        #     ('NH', 'NH'),
        #     ('NJ', 'NJ'),
        #     ('NM', 'NM'),
        #     ('NY', 'NY'),
        #     ('NC', 'NC'),
        #     ('ND', 'ND'),
        #     ('OH', 'OH'),
        #     ('OK', 'OK'),
        #     ('OR', 'OR'),
        #     ('MD', 'MD'),
        #     ('MA', 'MA'),
        #     ('MI', 'MI'),
        #     ('MN', 'MN'),
        #     ('MS', 'MS'),
        #     ('MO', 'MO'),
        #     ('PA', 'PA'),
        #     ('RI', 'RI'),
        #     ('SC', 'SC'),
        #     ('SD', 'SD'),
        #     ('TN', 'TN'),
        #     ('TX', 'TX'),
        #     ('UT', 'UT'),
        #     ('VT', 'VT'),
        #     ('VA', 'VA'),
        #     ('WA', 'WA'),
        #     ('WV', 'WV'),
        #     ('WI', 'WI'),
        #     ('WY', 'WY'),
        # ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        # phone number regex https://ihateregex.io/expr/phone
        'phone', validators=[DataRequired(),
                             Regexp("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",message='Please Enter a Valid phone number')]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired(),AnyOf([ choice.value for choice in Genres])],
          choices = Genres.choices()
        # choices=[
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'webiste', validators=[URL()]
    )
    image_link = StringField(
        'image_link'
    )
    is_seeking_talent = SelectField(
        'is_seeking_talent', validators=[DataRequired()],
        choices=[
            (True, 'Yes'),
            (False, 'No'),
        ]
    )
    
    seeking_description = StringField(
        'seeking_description'
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(),AnyOf([ choice.value for choice in State])],
          choices=State.choices()
        # choices=[
        #     ('AL', 'AL'),
        #     ('AK', 'AK'),
        #     ('AZ', 'AZ'),
        #     ('AR', 'AR'),
        #     ('CA', 'CA'),
        #     ('CO', 'CO'),
        #     ('CT', 'CT'),
        #     ('DE', 'DE'),
        #     ('DC', 'DC'),
        #     ('FL', 'FL'),
        #     ('GA', 'GA'),
        #     ('HI', 'HI'),
        #     ('ID', 'ID'),
        #     ('IL', 'IL'),
        #     ('IN', 'IN'),
        #     ('IA', 'IA'),
        #     ('KS', 'KS'),
        #     ('KY', 'KY'),
        #     ('LA', 'LA'),
        #     ('ME', 'ME'),
        #     ('MT', 'MT'),
        #     ('NE', 'NE'),
        #     ('NV', 'NV'),
        #     ('NH', 'NH'),
        #     ('NJ', 'NJ'),
        #     ('NM', 'NM'),
        #     ('NY', 'NY'),
        #     ('NC', 'NC'),
        #     ('ND', 'ND'),
        #     ('OH', 'OH'),
        #     ('OK', 'OK'),
        #     ('OR', 'OR'),
        #     ('MD', 'MD'),
        #     ('MA', 'MA'),
        #     ('MI', 'MI'),
        #     ('MN', 'MN'),
        #     ('MS', 'MS'),
        #     ('MO', 'MO'),
        #     ('PA', 'PA'),
        #     ('RI', 'RI'),
        #     ('SC', 'SC'),
        #     ('SD', 'SD'),
        #     ('TN', 'TN'),
        #     ('TX', 'TX'),
        #     ('UT', 'UT'),
        #     ('VT', 'VT'),
        #     ('VA', 'VA'),
        #     ('WA', 'WA'),
        #     ('WV', 'WV'),
        #     ('WI', 'WI'),
        #     ('WY', 'WY'),
        # ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        # TODO implement validation logic for state
         # phone number regex https://www.codegrepper.com/code-examples/python/regex+pattern+validate+phone+number
        'phone', validators=[Regexp('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',message='Please Enter a Valid phone number')]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
         'genres', validators=[DataRequired(),AnyOf([ choice.value for choice in Genres])],
          choices = Genres.choices()
        # choices=[
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'webiste', validators=[URL()]
    )
    
    is_seeking_venue = SelectField(
        'is_seeking_venue', validators=[DataRequired()],
        choices=[
            (True, 'Yes'),
            (False, 'No'),
        ]
    )
    
    seeking_venue_messge = StringField(
        'seeking_venue_messge'
    )

