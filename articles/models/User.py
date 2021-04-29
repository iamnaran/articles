from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from articles import db, login_manager, ma
from flask_login import UserMixin
from flask import current_app
from marshmallow import fields, validate
import jwt

from articles.models import Post
from articles.models.Post import PostSchema
from articles.models.UserRoles import UserRoleSchema
from articles.models.Role import RoleSchema


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('timestamp', db.String, default=datetime.utcnow)
                     )


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.Integer, nullable=False, server_default='0')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commented_by', lazy=True)
    likes = db.relationship('PostLike', backref='liked_by', lazy=True)
    roles = db.relationship('Role', secondary='user_roles', backref='user_role')
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # user_followers = db.relationship('User',
    #                                  secondary=followers,
    #                                  secondaryjoin=(followers.c.followed_id == id),
    #                                  primaryjoin=(followers.c.follower_id == id),
    #                                  backref=db.backref('followers', lazy='dynamic'),
    #                                  lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

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

    @classmethod
    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @classmethod
    def follow(self, user, userToFollow):
        if not user.is_following(user, userToFollow):
            user.followed.append(userToFollow)

    @classmethod
    def unfollow(self, user, userToFollow):
        if user.is_following(user, userToFollow):
            user.followed.remove(userToFollow)

    @classmethod
    def is_following(self, user, userToFollow):
        return user.followed.filter(
            followers.c.followed_id == userToFollow.id).count() > 0

    @classmethod
    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(
            Post.date_poasted.desc())


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User

    id = fields.Integer(dump_only=True)
    user_type = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=40))
    email = fields.Email(required=True, help='Unique Email Required.')
    image_file = fields.String(required=False)
    posts = fields.Nested(PostSchema, many=True)
    role = fields.Nested(RoleSchema)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
