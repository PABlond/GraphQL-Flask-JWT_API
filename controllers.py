
from graphene import ObjectType, String, Boolean, Schema
from flask_graphql import GraphQLView
from db import Users
from utils import encode

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()
    login = String(email=String(), password=String())
    signup = String(email=String(), password=String())

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'
    
    def resolve_login(root, info, email, password):
        print(email, password)
        return 'true'
    
    def resolve_signup(root, info, email, password):
        # print(email, password)
        user = {'email': email, 'password': password}
        is_user_exist = Users.find_one(user)
        print(is_user_exist)
        if is_user_exist:
            return "User already exists"
        else: 
            Users.insert_one(user)
            token = encode(user = {"email": email})
            return token


view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))
