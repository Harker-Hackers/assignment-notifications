import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #email
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'schoologycalendar@gmail.com'
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD") or "123"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    #database
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False