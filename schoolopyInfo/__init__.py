import schoolopy
from os import getenv
from flask import url_for, request
from app import app
from app.models import User
from encrypter import decrypt_message
host=getenv("HOME_URL")

class scAuth:
    def __init__(self):
        self.schoolopyAuth = schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), three_legged=True, domain='https://schoology.harker.org/')
        self.schoolopyUrl = self.schoolopyAuth.request_authorization(callback_url=host+'/authorized')
    def setSc(self):
        if not self.schoolopyAuth.authorize():
            return False
        else:
            self.sc=schoolopy.Schoology(self.schoolopyAuth)

class scAuthVer:
    def __init__(self, user):
        my_user=User.query.filter_by(username=user).first()
        request_token=decrypt_message(my_user.token)
        request_token_secret=decrypt_message(my_user.token_secret)
        self.schoolopyAuth=schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), domain='https://schoology.harker.org/', access_token=request_token, access_token_secret=request_token_secret) 
        self.schoolopyUrl = self.schoolopyAuth.request_authorization(callback_url=host+'/authorized')
    def setSc(self):
        if not self.schoolopyAuth.authorize():
            return False
        else:
            self.sc=schoolopy.Schoology(self.schoolopyAuth)

class authDict:
    def __init__(self):
        self.verAuth={}
        self.fAuth={}
        self.aId=0
    def addTempAuth(self):
        auth=scAuth()
        self.fAuth[self.aId]=auth
        self.aId+=1
        return(auth,self.aId-1)
    def verifyAuth(self,authId, tok):
        authId=int(authId)
        auth=self.fAuth[authId]
        if not auth.schoolopyAuth.authorize():
            return False
        self.fAuth.pop(authId)
        auth.setSc()
        self.verAuth[tok]=auth
        return tok
    def getAuth(self,tok):
        try:
            return self.verAuth[tok]
        except Exception as e:
            print(e)
            return 0
    def clearAuth(self):
        self.verAuth={}
        self.fAuth={}
        self.aId=0
