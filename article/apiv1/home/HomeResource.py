from flask import request
from flask.json import jsonify
from flask_restx import Resource, Namespace
from article import db
import traceback


from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from article.models.Post import post_schema, Post, posts_schema

homePageApis = Namespace('home_apis', description='Home Page Api')


@homePageApis.route('/all')
@homePageApis.doc('Get Home Page Data')
class HomeResource(Resource):
    """Get Home Page API Delete & Update"""

    @jwt_required()
    def get(self):
        """Get All Post For Home Page"""
        try:
            posts = Post.getAllPostForHomePage()
            message = 'Home page api fetched successfully'
            return {'status': True, 'message': message, 'data': posts}
        except Exception as e:
            traceback.print_exc()
            message = f'Error occurred: {str(e)}'
            return {'status': False, 'message': message, 'data': "null"}