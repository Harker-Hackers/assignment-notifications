#limiter
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app import app

limiter=Limiter(app,key_func=get_remote_address,
default_limits=["200 per day", "50 per hour"])