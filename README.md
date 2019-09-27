# GraphQL-Flask-JWT_API

This repository is a boilerplate to deal with JWT authentication using Flask, GraphQL and MongoDB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install needed librairies.

```bash
pip install -r requirements.txt
```

## Usage

```bash
env FLASK_APP=app.py FLASK_DEBUG=1 flask run
```

Then, you can request the API as follows:

```GraphQL
{
    signup(email: <EMAIL>, password: <PASSWORD>) {
        _id
        email
        token
    }
    login(email: <EMAIL>, password: <PASSWORD>) {
        _id
        email
        token
    }
    user(token: <TOKEN>) {
        _id
        email
        token # A new token is requested with a new expiration date
    }
}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)