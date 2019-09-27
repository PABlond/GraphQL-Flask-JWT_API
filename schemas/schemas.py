from schemas.user import User
from graphene import String, Field


def query_auth_schemas():
    login = Field(User, email=String(), password=String())
    signup = Field(User, email=String(), password=String())
    user = Field(User, required=True, token=String(required=True))
    return login, signup, user