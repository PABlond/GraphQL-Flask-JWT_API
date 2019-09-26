import jwt
import os

JWT_SECRET = os.environ.get("JWT_SECRET")

def encode(user):
    return jwt.encode(user, JWT_SECRET, algorithm='HS256').decode("utf-8") 