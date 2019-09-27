from graphene import ObjectType, String, Boolean, ID, Schema, Field, Interface
from flask_graphql import GraphQLView
from db import Users
from utils import encode, decode, encrypt_password, decrypt_password


class User(ObjectType):
    _id = String(required=True)
    email = String(required=True)
    isCheck = Boolean(required=True)
    token = String()

    def resolve_isCheck(root, info):
        return root['is_check']

    def resolve_token(root, info):
        return encode(user={"email": root['email']})


class Query(ObjectType):
    login = Field(User, email=String(), password=String())
    signup = Field(User, email=String(), password=String())
    user = Field(User, required=True, token=String(required=True))

    def resolve_login(root, info, email, password):
        user = Users.find_one({"email": email})
        if user:
            if decrypt_password(password=password,
                                hashed_password=user['password']):
                return user
            else:
                raise Exception("Password incorrect")
        else:
            raise Exception('User not found')

    def resolve_signup(root, info, email, password):
        if Users.find_one({email: email}):
            raise Exception("User already exists")
        else:
            user = {
                'email': email,
                'password': encrypt_password(password=password),
                "is_check": False
            }
            _id = Users.insert_one(user)
            user['_id'] = _id.inserted_id
            print(user)
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


view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))
