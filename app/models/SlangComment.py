from datetime import datetime
from app import ma
from marshmallow import fields, validate

from app import db


class SlangComment(db.Model):
    __tablename__ = 'slang_comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    commented_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('slang_word.id'), nullable=False)

    def __init__(self, comment, user_id, word_id):
        self.comment = comment
        self.user_id = user_id
        self.word_id = word_id

    def __repr__(self):
        return f"User('{self.comment}','{self.commented_date}','{self.user_id}','{self.word_id}')"


class SlangCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = SlangComment
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    comment = fields.String(required=True)
    commented_date = fields.DateTime(required=True)
    commented_by = fields.Nested("UserSchema", only=("id", "username", "email"))
    word_id = fields.Integer()


commentSchema = SlangCommentSchema()
commentsSchema = SlangCommentSchema(many=True)
