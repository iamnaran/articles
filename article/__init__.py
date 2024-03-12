from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
import os
import psycopg2

from article.config import Config

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
    migrate = Migrate(app, db)

    with app.app_context():
        try:            
            print("---> Creating new tables")
            db.create_all()
            
            print("---> Applying migrations")
            migrate.init_app(app, db)
            upgrade()
    
            print("---> Database migration completed successfully")
        except Exception as e:
            print(f"Error occurred during database migration: {str(e)}")
            db.session.rollback()
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

    return app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)


