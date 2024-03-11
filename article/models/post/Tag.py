from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @staticmethod
    def getAllTags():
        tags = Tag.query.all()
        return tagsSchema.dump(tags)


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, help='Tag Name Required.')
    num_posts = fields.Integer()


tagschema = TagSchema()
tagsSchema = TagSchema(many=True)
