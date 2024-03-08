from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article.models.user.User import User

from article import db


class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)

    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = User.query.filter_by(jti=jti).first()
        return bool(query)

    def __repr__(self):
        return '<id: token: {}'.format(self.jti)


class TokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Blacklist
        load_instance = True

    id = fields.Number(dump_only=True)
    jti = fields.String(required=True)


tokenSchema = TokenSchema()
