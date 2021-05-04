from datetime import datetime
from article import ma
from marshmallow import fields, validate
from article.models.Comment import CommentSchema

from article import db
from article.models.PostLike import PostLikeSchema
from article.models.SlangComment import SlangCommentSchema
from article.models.SlangWordUpVote import SlangWordUpVoteSchema


class SlangWord(db.Model):
    __tablename__ = 'slang_word'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_expired = db.Column(db.Integer, nullable=False, server_default='0')
    date_poasted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('SlangComment', backref='comments', lazy=True)
    upvote = db.relationship('SlangWordUpVote', backref='upvote', lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.content}','{self.date_poasted}')"


class SlangWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = SlangWord
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, help='Title Required.')
    content = fields.String(required=True, help='Content Required.')
    date_poasted = fields.DateTime(dump_only=True)
    # user_id = fields.Integer()
    author = fields.Nested("UserSchema", only=("id", "username", "email"))
    comments = fields.Nested(SlangCommentSchema, many=True)
    upvote = fields.Nested(SlangWordUpVoteSchema, many=True)


slang_word_schema = SlangWordSchema()
slang_words_schema = SlangWordSchema(many=True)
