from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from articles.config import Config
from flask_moment import Moment
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
api = Api()
jwt = JWTManager()


login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(conf_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    api.init_app(app)
    jwt.init_app(app)

    from articles.api.endpoints_v1 import endpoints
    from articles.users.routes import users
    from articles.main.routes import main
    from articles.posts.routes import posts
    from articles.errors.handlers import errors
    from articles.api.endpoints_v1 import endpoints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(endpoints, url_prefix="/api/v1")

    return app
