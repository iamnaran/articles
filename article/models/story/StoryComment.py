from datetime import datetime

from marshmallow import fields

from article import db
from article import ma


class StoryComment(db.Model):
    __tablename__ = 'story-comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    commented_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    def __init__(self, comment, user_id, post_id):
        self.comment = comment
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f"User('{self.comment}','{self.commented_date}','{self.user_id}','{self.post_id}')"


class StoryCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = StoryComment
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    comment = fields.String(required=True)
    commented_date = fields.DateTime(required=True)
    commented_by = fields.Nested("UserSchema", only=("id", "username", "email"))
    post_id = fields.Integer()


commentSchema = StoryCommentSchema()
commentsSchema = StoryCommentSchema(many=True)
