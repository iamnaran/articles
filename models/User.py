import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from articles import db, login_manager, ma
from flask_login import UserMixin
from flask import current_app
from marshmallow import fields, validate
import jwt

from articles.models.Post import PostSchema


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='commented_by', lazy=True)

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

    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5, seconds=5),
                'iat': datetime.datetime.utcnow(),
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
    def find_by_Id(cls, user_id):

        return User.query.filter_by(id=user_id).first()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=40))
    email = fields.Email(required=True, help='Unique Email Required.')
    image_file = fields.String(required=False)
    posts = fields.Nested(PostSchema, many=True)


user_schema = UserSchema(only=("username", "email", "image_file"))
users_schema = UserSchema(many=True)
