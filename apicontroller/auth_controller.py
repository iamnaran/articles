import sys

from articles.models.User import User
from articles.models.User import users_schema, user_schema
from sqlalchemy import or_, and_

from articles import db, bcrypt


def registerUser(registeredUser):
    try:
        user = User.query.filter(
            or_(User.username == registeredUser.username, User.email == registeredUser.email)).first()
        if user:
            return False, "Username or email already registered.", "null", "null"
        else:
            db.session.add(registeredUser)
            db.session.commit()
            auth_token = User.encode_auth_token(user.id)
            return True, "User registered successfully.", user_schema.dump(registeredUser), auth_token

    except Exception as e:
        return False, e.args, "null", "null"


def loginUser(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                auth_token = User.encode_auth_token(user.id)
                return True, "User Logged In successfully.", "Bearer " + auth_token.decode(), user_schema.dump(user)
            else:
                return False, "Password doesn't match", "null", "null"
        else:
            return False, "Email not registered.", "null", "null"

    except Exception as e:
        return False, e.args


def check_auth_header(auth_header):
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return ''


# def check_is_jwt_valid(auth_header):

    # if  decode_and_verify_jwt(auth_header, is_access_token=True, check_csrf=False):
    #
    #     return True
    # else:
    #     return False
