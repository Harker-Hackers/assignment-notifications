'''
IMPORTANT
When changing the User class in any way, run the following locally:
flask db migrate
flask db upgrade
Then, run the following on heroku:
heroku run flask db upgrade
'''

#basic imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

#app
from app import app

#creating db and migrate
db = SQLAlchemy(app)
migrate=Migrate(app, db)

#base class
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    password=db.Column(db.String)
    discId=db.Column(db.Integer)
    data = db.relationship('Course', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(140))
    courseId=db.Column(db.Integer)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Course {}>'.format(self.name)