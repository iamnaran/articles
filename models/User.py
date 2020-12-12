import datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from articles import db, login_manager
from flask_login import UserMixin
from flask import current_app
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
import jwt

from articles.models.Post import PostSchema


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
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

    def save_to_db(self):

        db.session.add(self)

        db.session.commit()

    @classmethod
    def find_by_username(cls, username):

        return cls.query.filter_by(username=username).first()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User

    id = fields.Number(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=40))
    email = fields.String(required=True, help='Unique Email Required.')
    image_file = fields.String(required=False)

    posts = fields.Nested(PostSchema, many=True)


user_schema = UserSchema(only=("username", "email", "image_file"))
users_schema = UserSchema(many=True)
