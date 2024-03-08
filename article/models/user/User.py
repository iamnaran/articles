from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from article import db, login_manager, ma
from flask_login import UserMixin
from flask import current_app
from marshmallow import fields, validate
import jwt

from article.models.post import Post
from article.models.user import Follow

from article.models.post.Post import PostSchema
from article.models.user.UserRoles import UserRoleSchema
from article.models.user.Role import RoleSchema


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.Integer, nullable=False, server_default='0')
    username = db.Column(db.String(20), unique=True, nullable=False)
    idToken = db.Column(db.String(120), unique=True, nullable=False)
    userFrom = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commented_by', lazy=True)
    likes = db.relationship('PostLike', backref='liked_by', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower_user', lazy='dynamic')


    # user_followers = db.relationship('User',
    #                                  secondary=followers,
    #                                  secondaryjoin=(followers.c.followed_id == id),
    #                                  primaryjoin=(followers.c.follower_id == id),
    #                                  backref=db.backref('followers', lazy='dynamic'),
    #                                  lazy='dynamic')

    def __init__(self, username, idToken,userFrom, email, password):
        self.username = username
        self.idToken = idToken
        self.email = email
        self.userFrom = userFrom
        self.password = password

    @staticmethod
    def getUserById(userId):
        user = User.query.filter_by(id=userId).first()
        return user_schema.dump(user)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=10, seconds=5),
                'iat': datetime.now(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string

        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def find_by_Id(cls, user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def follow_user(self, user_id):
        """Follow another user."""
        if self.id == user_id:
            return False, 'You cannot follow yourself'

        if self.is_following(user_id):
            return False, 'You are already following this user'

        follow = Follow(follower_id=self.id, followed_id=user_id)
        db.session.add(follow)
        db.session.commit()
        return True, 'You are now following this user'

    def unfollow_user(self, user_id):
        """Unfollow another user."""
        follow = Follow.query.filter_by(follower_id=self.id, followed_id=user_id).first()
        if not follow:
            return False, 'You are not following this user'

        db.session.delete(follow)
        db.session.commit()
        return True, 'You have unfollowed this user'

    def is_following(self, user_id):
        """Check if the user is already following another user."""
        return Follow.query.filter_by(follower_id=self.id, followed_id=user_id).first() is not None



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User

    id = fields.Integer(dump_only=True)
    user_type = fields.Integer(dump_only=True)
    idToken = fields.String(required=True)
    userFrom = fields.String(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=40))
    email = fields.Email(required=True, help='Unique Email Required.')
    image_file = fields.String(required=False)
    posts = fields.Nested(PostSchema, many=True)


user_schema = UserSchema(only=("id", "username", "email", "image_file", "user_type", "idToken"))
users_schema = UserSchema(only=("id", "username", "email", "image_file", "user_type", "idToken"), many=True)
