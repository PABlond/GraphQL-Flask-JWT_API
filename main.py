from flask import Flask, escape, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_graphql import GraphQLView
from graphene import Schema
from resolvers import Query

load_dotenv()

app = Flask(__name__)

view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))

app.add_url_rule("/graphql", view_func=view_func)

if __name__ == "__main__":
    app.run() 