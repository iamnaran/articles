import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from article import db, login_manager, ma
from flask_login import UserMixin
from flask import current_app
from marshmallow import fields, validate
import jwt



class Follow(db.Model, UserMixin):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id'),nullable=False)
    followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id'),nullable=False)
    
    @staticmethod
    def getFollowerCountById(userId):
        follower = Follow.query.filter_by(followed_id = userId).all()
        if follower:
            return len(follower)
        else:
            return 0
    
    @staticmethod
    def getFollowingCountById(userId):
        following = Follow.query.filter_by(follower_id = userId).all()
        if following:
            return len(following)
        else:
            return 0

class FollowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Follow

    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer(dump_only=True)
    followed_id = fields.Integer(dump_only=True)


follow_schema = FollowSchema()
follows_Schema = FollowSchema(many=True)
