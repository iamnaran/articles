from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db

class BaseImage(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    base64_data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"BaseImage(id={self.id}, filename='{self.filename}')"
    


class BaseImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = BaseImage
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    filename = fields.String(required=True)
    base64_data = fields.String(required=True)


baseImageSchema = BaseImageSchema()
baseImagesSchema = BaseImageSchema(many=True)
