from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db

class PostLike(db.Model):
    __tablename__ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    clap_count = db.Column(db.Integer, default=0)


    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

    def __init__(self, user_id, post_id, clap_count):
        self.user_id = user_id
        self.post_id = post_id
        self.clap_count = clap_count

    def __repr__(self):
        return f"User('{self.updated_at}','{self.user_id}','{self.post_id}')"
    
    @staticmethod
    def getLikesByPostId(postId, userId):
        likes = PostLike.query.filter_by(post_id=postId, user_id = userId).all()
        return post_likes_schema.dump(likes)
    
    @staticmethod
    def getExistingClap(postId, userId):
        likes = PostLike.query.filter_by(user_id=userId,post_id=postId).first()
        return likes


class PostLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = PostLike
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    updated_at = fields.DateTime(required=True)
    liked_by = fields.Nested("UserSchema", only=("id", "username", "email"))
    post_id = fields.Integer()


post_like_schema = PostLikeSchema()
post_likes_schema = PostLikeSchema(many=True)
