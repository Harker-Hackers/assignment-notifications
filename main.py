#eventlet server for socketio
import eventlet
eventlet.monkey_patch()

#importing app
from app import app, socketio, db, migrate


#running app
if (__name__=="__main__"):
    #local environment
    socketio.run(app,host='0.0.0.0', port=80, debug=True)