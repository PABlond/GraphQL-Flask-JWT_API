# GraphQL-Flask-JWT_API

This repository is a boilerplate to deal with JWT authentication using Flask, GraphQL and MongoDB.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install needed librairies.

```bash
pip install -r requirements.txt
```

## Usage

```bash
env FLASK_APP=main.py flask run
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

example of login authentication : 

[{login(email:"john.doe@sample.net", password: "123") {email, token}}](https://graphql-flask-jwt-api.herokuapp.com/graphql?query={login(email:"john.doe@sample.net",%20password:%20"123")%20{email,%20token}})

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)