# import datetime
#
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from app import db, login_manager, ma
# from flask_login import UserMixin
# from flask import current_app
# from marshmallow import fields, validate
# import jwt
#
# from app.models import Post
# from app.models.Post import PostSchema
# from app.models.UserRoles import UserRoleSchema
# from app.models.Role import RoleSchema
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
#
# class Followers(db.Model, UserMixin):
#     __tablename__ = 'followers'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     follower_id = db.Column('follower_id', db.Integer, db.ForeignKey('user.id'))
#     followed_id = db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
#
#
# class FollowersSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         # Fields to expose
#         model = Followers
#
#     id = fields.Integer(dump_only=True)
#     follower_id = fields.Integer(dump_only=True)
#     followed_id = fields.Integer(dump_only=True)
#
#
# follower_schema = FollowersSchema()
# followers_schema = FollowersSchema(many=True)
