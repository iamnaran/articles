from datetime import datetime
from article import db

from article.models.post.Comment import CommentSchema
from article.models.post.PostLike import PostLike,post_like_schema,post_likes_schema
from article.models.post.Tag import Tag
from article.models.post.PostWithTags import post_tags

from article import ma
from marshmallow import fields, validate

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_poasted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('PostLike', backref='likes', lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.content}','{self.date_poasted}')"

    @staticmethod
    def get_all_post():
        return Post.query.all()

    @staticmethod
    def getAllPostByAuthorId(userId):
        posts = Post.query.filter_by(user_id=userId).all()
        return posts_schema.dump(posts)
    
    @staticmethod
    def getAllPostForHomePage():
        posts = Post.query.all()
        return posts_schema.dump(posts)

    @staticmethod
    def get_post_by_id(post_id):
        post = Post.query.get(post_id)
        return post_schema.dump(post)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Post
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, help='Title Required.')
    content = fields.String(required=True, help='Content Required.')
    date_poasted = fields.DateTime(dump_only=True)
    tags = fields.Nested("TagSchema", many=True, only=("id", "name"))
    author = fields.Nested("UserSchema", only=("id", "username", "email",), many=False)
    comments = fields.Nested(CommentSchema, many=True)
    likes = fields.Nested("PostLikeSchema", many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
