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

from article.models.post.Comment import commentSchema, Comment, commentsSchema

comment_apis = Namespace('comment_apis', description='Comment API')


@comment_apis.route('/<int:post_id>')
@comment_apis.doc('Get comment by post id & Delete Comment')
class CommentResource(Resource):
    """Comment Delete & Update"""
    
    @jwt_required()
    def get(self, post_id):
        """Get a post with id"""
        try:
            post = Comment.getAllCommentsByPostId(post_id)
            message = 'Comments fetched successfully'
            return {'status': True, 'message': message, 'data': post}
        except:
            message = 'Error has occurred while requesting post'
            return {'status': False, 'message': message, 'data': "null"}


    def post(self, post_id):
        """Add Comment"""
        try:
            verify_jwt_in_request()
            comment = request.form['comment']

            try:
                comment = Comment(comment=comment, user_id=get_jwt_identity(), post_id=post_id)
                db.session.add(comment)
                db.session.commit()
                # post = post_controller.create_new_post(title=title, content=content, user_id=get_jwt_identity())
                if comment:
                    message = 'Commented successfully'
                    return {'status': True, 'message': message, 'data': commentSchema.dump(comment)}
                else:
                    message = 'Cannot Comment due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while commenting'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
