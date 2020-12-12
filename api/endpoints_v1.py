import pdb

from flask import Blueprint, request
from flask_restx import Api, Resource, reqparse
from marshmallow import ValidationError
from flask import jsonify
from articles import bcrypt
from articles.models.User import User, UserSchema, user_schema
from articles.models.Post import Post
from articles.models import RevokedToken
from articles.apicontroller import user_controller, post_controller, auth_controller

from flask_jwt import jwt_required, current_identity

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

endpoints = Blueprint('endpoints', __name__, url_prefix="/api/v1")

api = Api(endpoints, title="FLASK Articles  Rest API", version="1.0", description="FLASK RESTX API ")

ns = api.namespace("articles", description="Articles operations")


@api.errorhandler
def default_error_handler():
    message = 'An unhandled exception occurred.'
    return {'status': False, 'message': message}, 500


@ns.route("/users")
@api.doc('Users from articles')
class Users(Resource):
    """User List"""

    def get(self):
        """List all users"""
        message = 'User list fetched successfully'
        users = user_controller.get_all_users()
        return {'status': True, 'message': message, 'data': users}


@ns.route("/posts")
@api.doc('Post from articles')
class Posts(Resource):
    """Post List"""

    def get(self):
        """List all posts"""
        message = 'Post list fetched successfully'
        posts = post_controller.get_all_post()
        return {'status': True, 'message': message, 'data': posts}


@ns.route('/post/<int:post_id>')
@api.doc('Post from articles')
class postDetails(Resource):
    """Single posts"""

    def get(self, post_id):
        message = 'Post fetched successfully'
        post = post_controller.get_post_by_id(post_id)
        return {'status': True, 'message': message, 'data': post}

    def delete(self):
        message = 'Post deleted successfully'
        post_controller.get_all_post()
        return {'status': True, 'message': message, 'data': post}


@ns.route("/login")
@api.doc('Login user')
class LoginUser(Resource):

    def get(self):
        return "TODO"

    def post(self):

        try:
            email = request.form['email']
            password = request.form['password']
            status, message, auth_token, user = auth_controller.loginUser(email, password)

            return {'status': status, 'message': message, 'data': user, 'auth_token': auth_token.decode()}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@ns.route("/register-user")
@api.doc('Register user')
class RegisterUser(Resource):

    def get(self):
        return "TODO"

    def post(self):

        try:
            result = UserSchema().load(request.form)
            hash_password = bcrypt.generate_password_hash(result['password']).decode('utf-8')

            user = User(username=result['username'], email=result['email'], password=hash_password)
            status, message, registered_user = auth_controller.registerUser(user)

            if status:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                user_dict = {'access_token': access_token, 'refresh_token': refresh_token}
                user_dict['user'] = registered_user

                return jsonify({'status': status, 'message': message,
                                'data': user_dict})
            else:
                return jsonify({'status': status, 'message': message})

            # return {'status': status, 'message': message, 'has_password': hash_password, 'username': result['username']}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@ns.route("/token-refresh")
@api.doc('Token Refresh')
class TokenRefresh(Resource):
    """
    Token Refresh Api
    """

    @jwt_refresh_token_required
    def post(self):
        # Generating new access token
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user)

        return {'access_token': access_token}


@ns.route("/logout")
@api.doc('Logout Api')
class UserLogoutAccess(Resource):
    """
    User Logout Api
    """

    @jwt_required
    def post(self):

        jti = get_raw_jwt()['jti']

        try:
            # Revoking access token
            revoked_token = RevokedToken(jti=jti)

            revoked_token.add()

            return {'status': False, 'message': 'Access token has been revoked'}

        except:

            return {'status': False, 'message': 'Something went wrong'}, 500


@ns.route("/logout-refresh")
@api.doc('Logout Api')
class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api
    """

    @jwt_refresh_token_required
    def post(self):

        jti = get_raw_jwt()['jti']

        try:

            revoked_token = RevokedToken(jti=jti)

            revoked_token.add()

            pdb.set_trace()

            return {'status': False, 'message': 'Refresh token has been revoked'}

        except:

            return {'status': False, 'message': 'Something went wrong'}, 500


@ns.route("/post/create", methods=['POST'])
@api.doc('Create Post articles')
class Posts(Resource):
    """Post List"""

    def create(self):
        """List all posts"""
        data = request.get_json()

        message = 'Post list fetched successfully'
        posts = post_controller.get_all_post()
        return {'status': True, 'message': message, 'data': posts}


@ns.route("/jwt-test", methods=['GET'])
@api.doc('JWT TEST')
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }

