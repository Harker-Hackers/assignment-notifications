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