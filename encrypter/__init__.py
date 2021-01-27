#cryptography
from cryptography.fernet import Fernet
import os

def get_key():
    k=os.environ.get("TOKEN_ENCRYPT_KEY") or "x0nmJvWQLtblTEgCANbVaA7TPrPONzy_aVBX9w57ZOw="
    return k.encode()

def encrypt_message(message):
    f = Fernet(get_key())
    msg = message.encode()
    return f.encrypt(msg).decode()

def decrypt_message(message):
    f=Fernet(get_key())
    return f.decrypt(message.encode()).decode()