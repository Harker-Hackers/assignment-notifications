import schoolopy
from os import getenv
from flask import Flask, redirect


auth = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/')
url = auth.request_authorization(callback_url="localhost"+'/authorized')
app=Flask(__name__)
@app.route("/login")
def login():
    return redirect(url)

@app.route("/authorized")
def authorized():
    auth.authorize()
    tok=auth.access_token
    sec=auth.access_token_secret
    auth2 = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/', access_token=tok, access_token_secret=sec)
    auth2.oauth.token = {'oauth_token': tok, 'oauth_token_secret': sec}
    sc=schoolopy.Schoology(auth)
    sc2=schoolopy.Schoology(auth2)
    print(sc.get_me().username)
    #user1
    print(sc2.get_me().username)
    #owner of api
    return(".")
    
app.run(host="0.0.0.0",port=80)