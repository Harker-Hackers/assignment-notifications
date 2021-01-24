#modules
import eventlet
eventlet.monkey_patch()
from flask import Flask
from flask_socketio import SocketIO

#app
app = Flask(__name__)

#socketio engine
socketio=SocketIO(app,async_mode="eventlet", engineio_logger=False)

#routes
from app import routes