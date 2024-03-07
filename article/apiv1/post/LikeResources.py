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

from article.models.Post import post_schema, Post, posts_schema
from article.models.PostLike import post_like_schema, PostLike, post_likes_schema



likeapis = Namespace('likeapis', description='Like API')


@likeapis.route('/<int:post_id>')
@likeapis.doc('Like/ Unlike Post')
class LikeResources(Resource):
    """Like Delete & Update"""
    
    @jwt_required()
    def post(self, post_id):
        try:

            current_user_id = get_jwt_identity()
            
            # Check if the user has already liked the post
            existing_like = PostLike.getExistingClap(postId=post_id, userId= current_user_id)

            if existing_like:
                clap_limit = 50
                user_claps_count = existing_like.clap_count
                if user_claps_count >= clap_limit:
                    return {'status': False, 'message': 'You have reached the limit of claps for this post'}, 400
                # Increment the clap count
                existing_like.clap_count += 1
                db.session.commit()
                return {'status': True, 'message': 'You have clapped again for this post'}, 200
            
            
            # Add a new clap
            like = PostLike(user_id=current_user_id, post_id=post_id, clap_count=1)
            db.session.add(like)
            db.session.commit()
            
            return {'status': True, 'message': 'Post clapped successfully'}, 200
        except:
            return {'status': False, 'message': 'Error in clapping'}, 400

