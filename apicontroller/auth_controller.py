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
            return False, "Username or email already registered.", "null"
        else:
            db.session.add(registeredUser)
            db.session.commit()
            return True, "User registered successfully.", user_schema.dump(registeredUser)

    except Exception as e:
        return False, e.args


def loginUser(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                auth_token = User.encode_auth_token(user.id)
                return True, "User Logged In successfully.", auth_token, user_schema.dump(user)
            else:
                return False, "Password doesn't match", "null", "null"
        else:
            return False, "Email not registered.", "null", "null"

    except Exception as e:
        return False, e.args
