import schoolopy
from os import getenv
from flask import url_for, request
from app import app
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

class authDict:
    def __init__(self):
        self.verAuth={}
        self.fAuth={}
        self.aId=0
    def addTempAuth(self):
        auth=scAuth()
        self.fAuth[self.aId]=auth
        self.aId+=1
        print(self.fAuth)
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

def check_for_existing_auth(self, request_token, request_token_secret):
    try:
        schoolopy.Auth(getenv('SCHOOLOGY_KEY'), getenv('SCHOOLOGY_SECRET'), domain='https://schoology.harker.org/', request_token=request_token, request_token_secret=request_token_secret) 
        '''
        Request tokenn is retrieved from `schoolopy.Auth.request_token_secret and request_token`.
        After regulary authorizing with 3-legged, a class variable request_token_secret and request_token is
        given. This is what we will store in the DB.
        I'm not sure if we set three_legged to true of false though
        '''
    except:
        pass