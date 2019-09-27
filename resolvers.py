from graphene import ObjectType, String, Boolean, ID, Field, Interface
from config.db import Users
from services.utils import encode, decode, encrypt_password, decrypt_password
from schemas.schemas import User, query_auth_schemas


class Query(ObjectType):
    (login, signup, user) = query_auth_schemas()

    def resolve_login(root, info, email, password):
        user = Users.find_one({"email": email.lower()})
        if user:
            if decrypt_password(password=password,
                                hashed_password=user['password']):
                return user
            else:
                raise Exception("Password incorrect")
        else:
            raise Exception('User not found')

    def resolve_signup(root, info, email, password, firstname, lastname):
        print(email, password, firstname, lastname)
        if Users.find_one({"email": email.lower()}):
            raise Exception("User already exists")
        else:
            user = {
                'email': email.lower(),
                'password': encrypt_password(password=password),
                "firstname": firstname,
                "lastname": lastname,
                "is_check": False
            }
            _id = Users.insert_one(user)
            user['_id'] = _id.inserted_id
            return user

    def resolve_user(root, info, token):
        decoded = decode(token)
        if decoded:
            user = Users.find_one({"email": decoded['email']})
            if user:
                return user
            else:
                raise Exception("User not found")
        else:
            raise Exception("Invalid token")
