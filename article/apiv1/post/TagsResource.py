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

from article.models.post.Tag import tagschema, Tag, tagsSchema


tags_apis = Namespace('tags_apis', description='Post related operations')


@tags_apis.route('/all')
@tags_apis.doc('Get all tags & Create New tag')
class PostResources(Resource):
    """Tag Create & Listing"""

    def get(self):
        """List all tags"""
        tags = Tag.query.all()
        for tag in tags:
            tag.num_posts = tag.posts.count()
        message = 'Tags fetched successfully'
        return {'status': True, 'message': message, 'data': tagsSchema.dump(tags)}