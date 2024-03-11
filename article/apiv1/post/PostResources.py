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

from article.models.post.Tag import tagsSchema, Tag, tagschema
from article.models.post.Post import post_schema, Post, posts_schema


post_apis = Namespace('post_apis', description='Post related operations')


@post_apis.route('/post')
@post_apis.doc('Get all post & Create New Post')
class PostResources(Resource):
    """Post Create & List"""

    def get(self):
        """List all posts"""

        all_posts = Post.get_all_post()
        message = 'Post list fetched successfully'
        return {'status': True, 'message': message, 'data': posts_schema.dump(all_posts)}

    def post(self):
        """List all posts"""
        try:
            verify_jwt_in_request()
            title = request.form['title']
            content = request.form['content']
            tags_input = request.form['tags'].split(',')

            try:
                tags = []
                for tag_name in tags_input:
                    tag = Tag.query.filter_by(name=tag_name.strip()).first()
                    if not tag:
                        tag = Tag(name=tag_name.strip())
                        db.session.add(tag)
                    tags.append(tag)
                

                post = Post(title=title, content=content, user_id=get_jwt_identity())
                post.tags.extend(tags)
                db.session.add(post)
                db.session.commit()

                if post:
                    message = 'Posted successfully'
                    return {'status': True, 'message': message, 'data': post_schema.dump(post)}
                else:
                    message = 'Cannot Post'
                    return {'status': True, 'message': message, 'data': "null"}
            except:
                message = 'Error has occurred while posting'
                return {'status': True, 'message': message, 'data': "null"}

        except Exception as err:
            return {'status': False, 'message': err.args[0]}

