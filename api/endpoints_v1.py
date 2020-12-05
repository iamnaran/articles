from flask import Blueprint
from flask_restx import Api, Resource
from articles.controller import user_controller, post_controller

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

    def create(self):
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

