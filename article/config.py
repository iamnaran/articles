class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    # SQLALCHEMY_DATABASE_URI = 'postgres://mbtvzcprihywhg:d315f76c846d473fd9d9e39780ee2f07fe4082229b00ce8d03bdf67ed4f0e2f3@ec2-54-225-190-241.compute-1.amazonaws.com:5432/d3uno04qqo0h06'
    # SQLALCHEMY_DATABASE_URI = 'postgres://kkgpsgwj:IuZxh4_VBl-gxyMcgkrlF76XPr7prTg1@berry.db.elephantsql.com/kkgpsgwj'
    SQLALCHEMY_DATABASE_URI = 'postgresql://avnadmin:AVNS_eh0a2g6oRScQxc4xvWr@article-nrn-66f3.a.aivencloud.com:15151/defaultdb?sslmode=require'

    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/articles'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///article.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '574'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'delphiclab@gmail.com'
    MAIL_PASSWORD = '********'
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = 'image/*'
    DROPZONE_REDIRECT_VIEW = 'results'

    UPLOAD_FOLDER = '/static'
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
