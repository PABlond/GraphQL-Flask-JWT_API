from schemas.user import User
from graphene import String, Field, Boolean


def query_auth_schemas():
    login = Field(User, email=String(), password=String())
    signup = Field(User,
                   email=String(),
                   password=String(),
                   firstname=String(),
                   lastname=String())
    user = Field(User, required=True, token=String(required=True))
    userConfirm = Boolean(uniqid=String(), email=String())
    confirmResend = Boolean(email=String())
    return login, signup, user, userConfirm, confirmResend