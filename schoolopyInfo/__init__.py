import schoolopy
from os import getenv
from flask import url_for, request
from app import app
schoolopyAuth = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/')
host=getenv("HOME_URL")
schoolopyUrl = schoolopyAuth.request_authorization().replace('https%3A%2F%2Fschoology.harker.org%2F', host+"/authorize")
