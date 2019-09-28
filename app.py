from flask import Flask, escape, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_graphql import GraphQLView
from graphene import Schema
from resolvers import Query
from flask_cors import CORS
import schedule
import time


def job():
    print("I'm working...")


schedule.every(5).minutes.do(job)

load_dotenv()

app = Flask(__name__)
CORS(app)

view_func = GraphQLView.as_view("/graphql", schema=Schema(query=Query))

app.add_url_rule("/graphql", view_func=view_func)


@app.route('/')
def index():
    return "GraphQL server is listening on /graphql"


while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    app.run()
