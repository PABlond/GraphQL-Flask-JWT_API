import requests
import urllib.parse
import random
import string
from db import Users


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


url = "http://localhost:5000"
email = randomString(50)


def test_root_endpoint():
    r = requests.get('{}/'.format(url))
    print(r)
    assert r.status_code == 200


def test_signup_success():
    query = "{signup(email: \"" + email + "\", password: \"123\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))

    assert r.status_code == 200


def test_signup_exists():
    query = "{signup(email: \"john.doe@sample.net\", password: \"123\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))

    assert len(r.json()['errors']) == 1
    assert r.json()['errors'][0]['message'] == "User already exists"


def test_login_success():
    query = "{login(email:\"" + email + "\", password: \"123\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))

    Users.delete_one({"email": email})
    assert r.status_code == 200


def test_login_wrong_password():
    query = "{login(email: \"john.doe@sample.net\", password: \"1234\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))

    assert len(r.json()['errors']) == 1
    assert r.json()['errors'][0]['message'] == "Password incorrect"


def test_login_no_user():
    query = "{login(email:\"" + email + "\", password: \"123\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))

    assert len(r.json()['errors']) == 1
    assert r.json()['errors'][0]['message'] == "User not found"


def test_user_success():
    query_user = "{login(email:\"john.doe@sample.net\", password: \"123\") {email, token}}"
    r = requests.get("{}/graphql?query={}".format(
        url, urllib.parse.quote(query_user)))
    token = r.json()['data']['login']['token']

    query = "{user(token: \"" + token + "\") { token }}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))
    assert r.status_code == 200


def test_user_wrong_token():
    query = "{user(token: \"" + randomString(50) + "\") { token }}"
    r = requests.get("{}/graphql?query={}".format(url,
                                                  urllib.parse.quote(query)))
    assert len(r.json()['errors']) == 1
    assert r.json()['errors'][0]['message'] == "Invalid token"