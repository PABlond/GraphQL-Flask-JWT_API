from graphene import ObjectType, String, Boolean, Schema, Field
from flask_graphql import GraphQLView
from db import Users
from utils import encode, decode, encrypt_password, decrypt_password


class User(ObjectType):
    token = String()
    email = String()

    def resolve_token(parent, info):
        return "dzqdqzdqz"

    def resolve_email(parent, info):
        return "parent.email"


class Query(ObjectType):
    login = String(email=String(), password=String())
    signup = String(email=String(), password=String())
    user = String(token=String())

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

        if Users.find_one({email: user['email']}):
            return "User already exists"
        else:
            Users.insert_one(user)
            token = encode(user={"email": email})
            return token

    def resolve_user(root, info, token):
        print(decode(token))
        decoded = decode(token)
        if decoded:
            email = decoded['email']
            user = Users.find_one({"email": email})
            if user:
                return encode(user={"email": email})
            else: 
                return "User not found"            
        else:             
            return "Invalid token"


view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))
