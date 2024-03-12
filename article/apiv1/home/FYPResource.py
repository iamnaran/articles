from collections import defaultdict
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

from article.models.post.Post import post_schema, Post, posts_schema
from article.models.user.User import users_schema, User, user_schema
from article.models.post.PostLike import PostLike, post_like_schema, post_likes_schema
from article.models.post.Comment import Comment, commentSchema, commentsSchema




fyp_apis = Namespace('fyp_apis', description='For you page api')


@fyp_apis.route('/you')
@fyp_apis.doc('For You Page')
class HomeResource(Resource):
    """Fyp Api"""

    @jwt_required()
    def get(self):
        """Get For You """
        try:
            user_id = get_jwt_identity()            
            user = User.getUserById(user_id)
            post_scores = defaultdict(int)
             # Calculate scores for posts based on user preferences and interactions
            for post in Post.query.all():
                # Fetch likes for the current post
                likes_count = PostLike.query.filter_by(post_id=post.id).count()
                # Fetch comments for the current post
                comments_count = Comment.query.filter_by(post_id=post.id).count()
                
                # Score based on post popularity (e.g., likes, comments)
                post_scores[post.id] += likes_count * 2  # Double the weight for likes
                post_scores[post.id] += comments_count  # Count comments     
                            
            sorted_posts = sorted(post_scores.items(), key=lambda x: x[1], reverse=True)
            
            sorted_post_objects = [Post.query.get(post_id) for post_id, _ in sorted_posts]            
            
            # Serialize the posts using PostSchema
            serialized_posts = posts_schema.dump(sorted_post_objects)
            
            message = 'FYP fetched successfully'
            return {'status': True, 'message': message, 'data': serialized_posts}
        except Exception as e:
            traceback.print_exc()
            message = f'Error occurred: {str(e)}'
            return {'status': False, 'message': message, 'data': "null"}