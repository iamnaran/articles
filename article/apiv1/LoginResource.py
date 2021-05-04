from flask import request
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

from article.models.User import user_schema, User

auth_apis = Namespace('auth_apis', description='Auth related operations')


@auth_apis.route("/login")
@auth_apis.doc('Login user')
class LoginResource(Resource):

    def get(self):
        return "TODO"

    def post(self):

        try:
            email = request.form['email']
            password = request.form['password']
            try:
                user = User.find_by_email(email=email)

                if user:
                    if bcrypt.check_password_hash(user.password, password):
                        auth_token = create_access_token(identity=user.id)
                        refresh_token = create_refresh_token(identity=user.id)
                        message = 'Logged In Successfully'
                        return {'status': True, 'message': message, 'data': user_schema.dump(user),
                                'auth_token': "Bearer " + auth_token, 'refresh_token': "Bearer " + refresh_token}

                    else:
                        message = 'Password doesnt match with email.'
                        return {'status': False, 'message': message}
                else:
                    message = 'We cannot find user registered with this email'
                    return {'status': False, 'message': message}

            except Exception as e:
                message = 'Email and Password Field required'
                return {'status': False, 'message': message + str(e.args)}

        except Exception as e:
            return {'status': False, 'message': str(e.args)}
