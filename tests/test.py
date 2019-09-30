import requests
import urllib.parse

url = "http://localhost:5000"
query_user = "{login(email:\"john.doe@sample.net\", password: \"123\") {email, token}}"
r = requests.get("{}/graphql?query={}".format(url, urllib.parse.quote(query_user)))
token = r.json()['data']['login']['token']

query = "{user(token: \"" + token + "\") { token }}"
print(query)
r = requests.get("{}/graphql?query={}".format(url, urllib.parse.quote(query)))

print(r.json())