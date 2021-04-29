from datetime import datetime
from articles import ma
from marshmallow import fields, validate

from articles import db


class SlangWordUpVote(db.Model):
    __tablename__ = 'slang_upvote'

    id = db.Column(db.Integer, primary_key=True)
    is_liked = db.Column(db.Boolean, server_default='False', default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('slang_word.id'), nullable=False)

    def __init__(self, is_liked, user_id, word_id):
        self.is_liked = is_liked
        self.user_id = user_id
        self.word_id = word_id

    def __repr__(self):
        return f"User('{self.is_liked}','{self.updated_at}','{self.user_id}','{self.word_id}')"


class SlangWordUpVoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = SlangWordUpVote
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    is_liked = fields.Boolean(required=True)
    updated_at = fields.DateTime(required=True)
    word_id = fields.Integer(required=True)
    liked_by = fields.Nested("UserSchema", only=("id", "username", "email"))


slang_upvote_schema = SlangWordUpVoteSchema()
slang_upvotes_schema = SlangWordUpVoteSchema(many=True)
