from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db


class PostLike(db.Model):
    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    is_liked = db.Column(db.Boolean, server_default='False', default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, is_liked, user_id, post_id):
        self.is_liked = is_liked
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f"User('{self.is_liked}','{self.updated_at}','{self.user_id}','{self.post_id}')"


class PostLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = PostLike
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    is_liked = fields.Boolean(required=True)
    updated_at = fields.DateTime(required=True)
    liked_by = fields.Nested("UserSchema", only=("id", "username", "email"))
    post_id = fields.Integer()


post_like_schema = PostLikeSchema()
post_likes_schema = PostLikeSchema(many=True)
