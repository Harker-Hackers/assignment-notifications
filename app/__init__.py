#modules
import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO

#app
app = Flask(__name__)

#config
from app.config import Config
app.config.from_object(Config)

#db
from app.models import db, migrate

#socketio engine
socketio=SocketIO(app,async_mode="eventlet", engineio_logger=False)

#routes
from app import routes