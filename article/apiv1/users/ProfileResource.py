from flask import request
from flask.json import jsonify
from flask_restx import Resource, Namespace
from article import db

from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from article.models.user.User import user_schema, User, users_schema
from article.models.user.Follow import follow_schema, Follow, follows_Schema
from article.models.post.Post import post_schema, Post, posts_schema



profile_apis = Namespace('profile_apis', description='User Followers related operations')

@profile_apis.route('/<int:user_id>')
@profile_apis.doc('User Profile Details')
class PostResources(Resource):

    @jwt_required()
    def get(self, user_id):
        try:
            # Get the user by user_id
            user = User.getUserById(userId = user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            # Get the count of followers
            follower_count = Follow.getFollowerCountById(userId= user_id)

            # Get the count of following
            following_count = Follow.getFollowingCountById(userId= user_id)

            # Get the user's posts
            user_posts = Post.getAllPostByAuthorId(userId=user_id)

            # Serialize user data
            data = {
                'user': user,
                'follower_count': follower_count,
                'following_count': following_count,
                'posts': user_posts
            }

            return {'status': True, 'data': data}, 200


        except Exception as e:
            return {'status': False, 'message': f'An error occurred: {str(e)}'}, 500
