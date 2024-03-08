from flask import request
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

from article.models.user.Follow import follow_schema, Follow, follows_Schema

follow_apis = Namespace('follow_apis', description='User Followers related operations')

@follow_apis.route('/<int:user_id>')
@follow_apis.doc('Follow and Unfollow User')
class PostResources(Resource):
    """Follow and Unfollow users"""
    @staticmethod
    def follow_user(current_user_id, user_id):
        # Check if the user is trying to follow themselves
        if current_user_id == user_id:
            return {'status': False, 'message': 'You cannot follow yourself'}, 400
        
        # Check if the follow relationship already exists
        existing_follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()
        if existing_follow:
            return {'status': False, 'message': 'You are already following this user'}, 400
        
        # Create a new follow relationship
        follow = Follow(follower_id=current_user_id, followed_id=user_id)
        db.session.add(follow)
        db.session.commit()
        
        return {'status': True, 'message': 'You are now following this user'}, 200

    @staticmethod
    def unfollow_user(current_user_id, user_id):
        # Check if the follow relationship exists
        existing_follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=user_id).first()
        if not existing_follow:
            return {'status': False, 'message': 'You are not following this user'}, 400
        
        # Delete the follow relationship
        db.session.delete(existing_follow)
        db.session.commit()
        
        return {'status': True, 'message': 'You have unfollowed this user'}, 200

    @jwt_required()
    def post(self, user_id):
        current_user_id = get_jwt_identity()
        
        try:
            response = self.follow_user(current_user_id, user_id)
            return response
        except Exception as e:
            return {'status': False, 'message': f'An error occurred: {str(e)}'}, 500

    @jwt_required()
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        
        try:
            response = self.unfollow_user(current_user_id, user_id)
            return response
        except Exception as e:
            return {'status': False, 'message': f'An error occurred: {str(e)}'}, 500
