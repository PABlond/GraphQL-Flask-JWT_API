from graphene import ObjectType, String, Boolean, ID, Field, Interface
from config.db import Users
from services.utils import encode, decode, encrypt_password, decrypt_password, send_confirmation
from schemas.schemas import User, query_auth_schemas
import uuid


class Query(ObjectType):
    (login, signup, user, userConfirm, confirmResend) = query_auth_schemas()

    def resolve_login(root, info, email, password):
        user = Users.find_one({"email": email.lower()})
        if user:
            if decrypt_password(password=password,
                                hashed_password=user['password']):
                return user
            else:
                raise Exception("Password incorrect")
        else:
            raise Exception('User not found')

    def resolve_signup(root, info, email, password, firstname, lastname):
        print(email, password, firstname, lastname)
        if Users.find_one({"email": email.lower()}):
            raise Exception("User already exists")
        else:
            id = str(uuid.uuid1())
            user = {
                'email': email.lower(),
                'password': encrypt_password(password=password),
                "firstname": firstname,
                "lastname": lastname,
                "is_check": {
                    "status": False,
                    "id": id
                },
            }
            send_confirmation(receiver_address=email, checking_id=id)
            _id = Users.insert_one(user)
            user['_id'] = _id.inserted_id
            return user

    def resolve_user(root, info, token):
        decoded = decode(token)
        if decoded:
            user = Users.find_one({"email": decoded['email']})
            if user:
                return user
            else:
                raise Exception("User not found")
        else:
            raise Exception("Invalid token")

    def resolve_userConfirm(root, info, uniqid, email):
        user = Users.find_one({"email": email.lower()})
        if user:
            if (uniqid == user['is_check']['id']):
                Users.update_one(
                    {"email": email.lower()},
                    {'$set': {
                        "is_check": {
                            "status": True,
                            "id": ""
                        }
                    }})
                return True
            else:
                raise Exception("Link is not correct")
        else:
            raise Exception("User not found")

    def resolve_confirmResend(root, info, email):
        user = Users.find_one({"email": email.lower()})
        if user:
            is_check = user['is_check']
            if not is_check['status'] and is_check['id']:
                send_confirmation(receiver_address=email,
                                  checking_id=is_check['id'])
                return True
            else:
                raise Exception("User is already confirmed")
        else:
            raise Exception("User not found")