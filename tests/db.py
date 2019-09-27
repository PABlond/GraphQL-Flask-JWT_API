from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DB_URL")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

uri = "mongodb://{}:{}@{}".format(DB_USERNAME, DB_PASSWORD, DB_URL)
mongo = MongoClient(uri, retryWrites=False)
Users = mongo['python_jwt'].users