'''\
How to use:
python email.py
requierd config vars:
    DATABASE_URL=<database url>
    TOKEN_ENCRYPT_KEY=key used to encrypt tokens (get from heroku config")
'''


import psycopg2
import os
import sys
import schoolopy
import os
from cryptography.fernet import Fernet

DB_URI=os.environ.get("DATABASE_URL")



def decrypt_message(message):
    f=Fernet(os.environ.get("TOKEN_ENCRYPT_KEY").encode())
    return f.decrypt(message.encode()).decode()


def sendEmailUser(user):
    access_token=decrypt_message(user[4])
    access_token_secret=decrypt_message(user[5])
    auth = schoolopy.Auth(os.getenv('SCHOOLOGY_KEY'), os.getenv('SCHOOLOGY_SECRET'), domain='https://schoology.harker.org/', access_token=access_token, access_token_secret=access_token_secret, three_legged=True) 
    auth.oauth.token = {'oauth_token': access_token, 'oauth_token_secret': access_token_secret}
    sc=schoolopy.Schoology(auth)
    print(sc.get_me())

conn=psycopg2.connect(DB_URI)
cur=conn.cursor()
cur.execute("SELECT * FROM \"user\";")

users=cur.fetchall()
for user in users:
    try:
        sendEmailUser(user)
    except Exception as e:
        raise e
        continue
    
    