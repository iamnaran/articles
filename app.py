from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    # SQLALCHEMY_DATABASE_URI = 'postgres://mbtvzcprihywhg:d315f76c846d473fd9d9e39780ee2f07fe4082229b00ce8d03bdf67ed4f0e2f3@ec2-54-225-190-241.compute-1.amazonaws.com:5432/d3uno04qqo0h06'
    SQLALCHEMY_DATABASE_URI = 'postgres://kkgpsgwj:IuZxh4_VBl-gxyMcgkrlF76XPr7prTg1@berry.db.elephantsql.com/kkgpsgwj'

    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/articles'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///article.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '574'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'smartgov.article@gmail.com'
    MAIL_PASSWORD = '********'
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
    DROPZONE_REDIRECT_VIEW = 'results'

    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    # JWT
    JWT_SECRET_KEY = 'jwt-secret-string'

    # ec2 - 54 - 225 - 190 - 241.
    # compute - 1.
    # amazonaws.com
    # Database
    # d3uno04qqo0h06
    # User
    # mbtvzcprihywhg
    # Port
    # 5432
    # Password
    # d315f76c846d473fd9d9e39780ee2f07fe4082229b00ce8d03bdf67ed4f0e2f3
    # URI
    # compute - 1.
    #     postgres://mbtvzcprihywhg:d315f76c846d473fd9d9e39780ee2f07fe4082229b00ce8d03bdf67ed4f0e2f3@ec2-54-225-190-241.compute-1.amazonaws.com:5432/d3uno04qqo0h06
    # Heroku
    # CLI
    # heroku
    # pg: psql


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
jwt = JWTManager()
mail = Mail()
config = Config()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app = Flask(__name__)
app.config.from_object(config)

ma.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
moment.init_app(app)
jwt.init_app(app)

from article.users.routes import users
from article.main.routes import main
from article.posts.routes import posts
from article.errors.handlers import errors

# API
from article.apiv1 import apis as api_v1

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)

# API
app.register_blueprint(api_v1)




if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)