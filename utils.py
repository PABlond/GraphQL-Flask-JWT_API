import jwt
import bcrypt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.environ.get("JWT_SECRET")


def encode(user):
    return jwt.encode({
        "email": user['email'],
        'exp': datetime.utcnow() + timedelta(hours=1)
    },
                      JWT_SECRET,
                      algorithm='HS256').decode("utf-8")


def decode(token):
    try:        
        return jwt.decode(token, JWT_SECRET, algorithm='HS256')
    except:
        return {}


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'),
                         bcrypt.gensalt()).decode('utf8')


def decrypt_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf8'),
                          hashed_password.encode('utf8'))
