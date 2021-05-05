from sqlalchemy import or_, and_

from flask import request, jsonify
from flask_restx import Resource, Namespace
from article import db, bcrypt

from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from article.models.Role import Role
from article.models.User import user_schema, User, UserSchema

auth_register_apis = Namespace('auth_register_apis', description='Auth related operations')


@auth_register_apis.route("/register")
@auth_register_apis.doc('Register user')
class RegisterResource(Resource):

    @staticmethod
    def post():
        try:
            response = UserSchema().load(request.form)
            username = response['username']
            email = response['email']
            hash_password = bcrypt.generate_password_hash(response['password']).decode('utf-8')
            new_user = User(username=username, email=email, password=hash_password)
            try:
                user = User.query.filter(
                    or_(User.username == new_user.username, User.email == new_user.email)).first()
                if user:
                    message = 'A user is already registered with this email or username.'
                    return {'status': False, 'message': message}
                else:
                    db.session.add(new_user)
                    db.session.commit()
                    access_token = create_access_token(identity=new_user.id)
                    refresh_token = create_refresh_token(identity=new_user.id)
                    user_dict = {'access_token': "Bearer " + access_token, 'refresh_token': "Bearer " + refresh_token,
                                 'user_info': user_schema.dump(new_user)}

                    message = 'A user has been registered successfully'
                    return {'status': True, 'message': message, 'data': user_dict}

            except Exception as e:
                message = 'Something went wrong. Please try again later '
                return {'status': False, 'message': message + str(e.args)}

        except Exception as e:
            return {'status': False, 'message': str(e.args)}
