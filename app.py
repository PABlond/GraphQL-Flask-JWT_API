from flask import Flask, escape, request
from flask_pymongo import PyMongo
from controllers import view_func
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.add_url_rule("/graphql", view_func=view_func)

# @app.route("/")
# def home_page():
#     online_users = mongo.db.users.find_one({"online": True})
#     print(online_users)
#     return "online_users"

if __name__ == "__main__":
    app.run()