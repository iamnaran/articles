from datetime import datetime
from articles import ma
from marshmallow import fields, validate
from articles.models.Comment import CommentSchema

from articles import db
from articles.models.PostLike import PostLikeSchema

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_poasted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('PostLike', backref='likes', lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.content}','{self.date_poasted}')"

    @staticmethod
    def get_all_post():
        return Post.query.all()

    @staticmethod
    def get_post_by_id(self, post_id):
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
    # user_id = fields.Integer()
    author = fields.Nested("UserSchema", only=("id", "username", "email",), many=False)
    comments = fields.Nested(CommentSchema, many=True)
    likes = fields.Nested(PostLikeSchema, many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
