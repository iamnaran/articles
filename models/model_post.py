from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from articles import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_poasted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.content}','{self.date_posted}')"


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Post
        include_relationships = True
        load_instance = True

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    date_poasted = fields.DateTime(required=True)
    user_id = fields.Integer()


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
