import requests
import urllib.parse
from db import Users

url = "http://localhost:5000"


def signup(email):
    query = "{signup(email: \"" + email + "\", password: \"123\", firstname:\"firstname\", lastname:\"lastname\") {email, token}}"
    return requests.get("{}/graphql?query={}".format(
        url, urllib.parse.quote(query)))


def delete_user(email):
    Users.delete_one({"email": email})
