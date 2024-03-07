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

from article.models.Post import post_schema, Post, post_schema

post_operation_apis = Namespace('post_operation_apis', description='Post related operations')


@post_operation_apis.route('/post/<int:post_id>')
@post_operation_apis.doc('Get post by id & Delete Post')
class PostOperationResource(Resource):
    """Post Delete & Update"""

    @jwt_required()
    def delete(self, post_id):
        try:
            verify_jwt_in_request()
            try:
                post = Post.get_post_by_id(post_id)

                current_user_id = get_jwt_identity()
            
                if post.user_id != current_user_id:
                    return {'status': False, 'message': 'Unauthorized to update this comment'}
                
                if post:
                    db.session.delete(post)
                    db.session.commit()
                    message = 'Posted deleted successfully'
                    return {'status': True, 'message': message, 'data': post_schema.dump(post)}
                else:
                    message = 'Cannot Post due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while updatinga'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
        
    @jwt_required()
    def get(self, post_id):
        """Get a post with id"""

        post = Post.get_post_by_id(post_id)
        message = 'Post fetched successfully'
        return {'status': True, 'message': message, 'data': post_schema.dump(post)}
    
    @jwt_required()
    def put(self, post_id):
        """Update a post with id"""
        try:
            verify_jwt_in_request()
            title = request.form['title']
            content = request.form['content']

            try:
                post = Post.get_post_by_id(post_id)

                current_user_id = get_jwt_identity()
            
                if post.user_id != current_user_id:
                    return {'status': False, 'message': 'Unauthorized to update this comment'}
                
                if post:
                    post.title = title
                    post.content = content
                    db.session.commit()
                    message = 'Posted updated successfully'
                    return {'status': True, 'message': message, 'data': post_schema.dump(post)}
                else:
                    message = 'Cannot Post due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while updating'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
        
    @jwt_required()
    def post(self):
        """List all posts"""
        try:
            verify_jwt_in_request()
            title = request.form['title']
            content = request.form['content']

            try:
                post = Post(title=title, content=content, user_id=get_jwt_identity())
                db.session.add(post)
                db.session.commit()
                # post = post_controller.create_new_post(title=title, content=content, user_id=get_jwt_identity())
                if post:
                    message = 'Posted successfully'
                    return {'status': True, 'message': message, 'data': post_schema.dump(post)}
                else:
                    message = 'Cannot Post due to some error. Please try again later..'
                    return {'status': False, 'message': message, 'data': "null"}
            except Exception as err:
                message = 'Error has occurred while posting'
                return {'status': False, 'message': message + str(err.args), 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': str(err.args)}
