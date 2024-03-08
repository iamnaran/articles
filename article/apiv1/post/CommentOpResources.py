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

comment_operation_apis = Namespace('comment_operation_apis', description='Comment related operations')


@comment_operation_apis.route('/comment/<int:comment_id>')
@comment_operation_apis.doc('Get commnet by id & Delete Commnet')
class CommentOpResource(Resource):
    """Comment Delete & Update"""
    @jwt_required()
    def delete(self, commentId):
        try:
            verify_jwt_in_request()
            try:
                comment = Comment.getCommentById(commentId)
                if comment:
                    db.session.delete(comment)
                    db.session.commit()
                    message = 'Comment deleted successfully'
                    return {'status': True, 'message': message}
                else:
                    message = 'Cannot Post due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while updatinga'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
        
    @jwt_required()
    def put(self, commentId):
        """Update a post with id"""
        try:
            verify_jwt_in_request()
            commentInput = request.form['comment']
            try:
                commnetData = Comment.getCommentById(commentId)
                current_user_id = get_jwt_identity()
            
                if commnetData.user_id != current_user_id:
                    return {'status': False, 'message': 'Unauthorized to update this comment'}
                
                if commnetData:
                    commnetData.comment = commentInput
                    db.session.commit()
                    message = 'Comment updated successfully'
                    return {'status': True, 'message': message, 'data': commentSchema.dump(commnetData)}
                else:
                    message = 'Cannot Comment due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while updating'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
       
   
    
        