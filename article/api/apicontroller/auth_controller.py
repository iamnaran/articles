import sys

from article.models.user.Role import Role
from article.models.user.UserRoles import UserRoles
from article.models.user.User import User
from article.models.user.User import users_schema, user_schema
from sqlalchemy import or_, and_
from flask import jsonify

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from article import db, bcrypt


def registerUser(username, email, hash_password):
    new_user = User(username=username, email=email, password=hash_password)
    try:
        user = User.query.filter(
            or_(User.username == new_user.username, User.email == new_user.email)).first()
        if user:
            return False, "Username or email already registered.", "null", "null"
        else:
            role = Role(role_name='User Agent')
            new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()
            auth_token = create_access_token(identity=new_user.id)
            return True, "User registered successfully.", user_schema.dump(new_user), str(auth_token)

    except Exception as e:
        return False, e.args[0], "null", "null"


def loginUser(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                auth_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                return True, "User Logged In successfully.", "Bearer " + str(auth_token), user_schema.dump(user)
            else:
                return False, "Password doesn't match", "null", "null"
        else:
            return False, "Email not registered.", "null", "null"

    except Exception as e:
        return False, e.args[0], "null", "null"


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
