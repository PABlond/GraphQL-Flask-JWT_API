from graphene import ObjectType, String, Boolean, Schema
from flask_graphql import GraphQLView
from db import Users
from utils import encode, decode, encrypt_password, decrypt_password


class Query(ObjectType):
    login = String(email=String(), password=String())
    signup = String(email=String(), password=String())

    def resolve_login(root, info, email, password):
        user = Users.find_one({"email": email})
        if user:
            if decrypt_password(password, user['password']):
                token = encode(user={"email": email})
                return token
            else:
                return "Password incorrect"
        else:
            return 'User not found'

    def resolve_signup(root, info, email, password):
        user = {
            'email': email,
            'password': encrypt_password(password=password)
        }
        is_user_exist = Users.find_one({email: user['email']})
        print(is_user_exist)
        if is_user_exist:
            return "User already exists"
        else:
            Users.insert_one(user)
            token = encode(user={"email": email})
            return token


view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))
