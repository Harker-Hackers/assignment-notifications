import schoolopy
from os import getenv
import flask

app = flask.Flask(__name__)
auth = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/')
url = auth.request_authorization().replace('https%3A%2F%2Fschoology.harker.org%2F', '')
@app.route('/')
def home():
    print(url)
    return flask.render_template('auth.jinja', auth_link=url)

@app.route('/authorized')
def authorized():
    return 'Hey gunkers'

app.run(debug=True)