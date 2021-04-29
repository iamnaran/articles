from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from app.config import Config
from flask_moment import Moment
from flask_marshmallow import Marshmallow
from flask_restx import Api
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
jwt = JWTManager()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(conf_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("nAME =" + current_app.name)

    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    jwt.init_app(app)

    from app.users.routes import users
    from app.main.routes import main
    from app.posts.routes import posts
    from app.errors.handlers import errors

    # API
    from app.apiv1 import apis as api_v1

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # API
    app.register_blueprint(api_v1)

    return app
