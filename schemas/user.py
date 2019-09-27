from graphene import ObjectType, String, Boolean
from services.utils import encode


class User(ObjectType):
    _id = String(required=True)
    email = String(required=True)
    firstname = String()
    lastname = String()
    isCheck = Boolean(required=True)
    token = String()

    def resolve_isCheck(root, info):
        return root['is_check']['status']

    def resolve_token(root, info):
        return encode(user={"email": root['email']})
