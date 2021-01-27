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
    token_secret=db.Column(db.String)
    token=db.Column(db.String)
    discId=db.Column(db.Integer)
    courses=db.Column(db.String)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

#get courses
def getUserCourse(user):
    crs=user.courses
    crs=crs[2:-2]
    crs=crs.replace("'", "")
    crs=crs.split(",")
    crs = [int(i) for i in crs]
    return crs