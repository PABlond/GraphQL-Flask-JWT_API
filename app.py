from flask import Flask, escape, request
from controllers import view_func
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get("DB_URL")
print(SECRET_KEY)

app = Flask(__name__)
app.add_url_rule("/graphql", view_func=view_func)

if __name__ == "__main__":
    app.run()