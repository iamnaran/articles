class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '574'
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'smartgov.app@gmail.com'
    MAIL_PASSWORD = '********'

    # JWT
    JWT_SECRET_KEY = 'jwt-secret-string'
