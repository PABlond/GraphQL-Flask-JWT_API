from graphene import ObjectType, String, Boolean, Schema, Field
from flask_graphql import GraphQLView
from db import Users
from utils import encode, decode, encrypt_password, decrypt_password


class Query(ObjectType):
    login = String(email=String(), password=String())
    signup = String(email=String(), password=String())
    user = String(token=String())

    def resolve_login(root, info, email, password):
        user = Users.find_one({"email": email})
        if user:
            if decrypt_password(password=password,
                                hashed_password=user['password']):
                return encode(user={"email": email})
            else:
                raise Exception("Password incorrect")
        else:
            raise Exception('User not found')

    def resolve_signup(root, info, email, password):
        if Users.find_one({email: email}):
            raise Exception("User already exists")
        else:
            Users.insert_one({
                'email': email,
                'password': encrypt_password(password=password)
            })
            return encode(user={"email": email})

    def resolve_user(root, info, token):
        print(decode(token))
        decoded = decode(token)
        if decoded:
            email = decoded['email']
            user = Users.find_one({"email": email})
            if user:
                return encode(user={"email": email})
            else:
                raise Exception("User not found")
        else:
            raise Exception("Invalid token")


view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))
