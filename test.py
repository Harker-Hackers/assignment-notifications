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
    print(auth.authorize())
    tok=auth.access_token
    sec=auth.access_token_secret
    print(tok,sec)
    auth2 = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=False, domain='https://schoology.harker.org/', request_token=tok, request_token_secret=sec)
    print(auth2.authorize())
    sc=schoolopy.Schoology(auth)
    #sc2=schoolopy.Schoology(auth2)
    print(sc.get_me().username)
    #print(sc2.get_me().username)
    return(".")
    
app.run(host="0.0.0.0",port=80)