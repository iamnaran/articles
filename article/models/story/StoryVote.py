from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db


class StoryVote(db.Model):
    __tablename__ = 'story-vote'

    id = db.Column(db.Integer, primary_key=True)
    is_liked = db.Column(db.Boolean, server_default='False', default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    def __init__(self, is_liked, user_id, story_id):
        self.is_liked = is_liked
        self.user_id = user_id
        self.story_id = story_id

    def __repr__(self):
        return f"User('{self.is_liked}','{self.updated_at}','{self.user_id}','{self.story_id}')"


class StoryVoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = StoryVote
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    is_liked = fields.Boolean(required=True)
    updated_at = fields.DateTime(required=True)
    word_id = fields.Integer(required=True)
    liked_by = fields.Nested("UserSchema", only=("id", "username", "email"))


story_vote_schema = StoryVoteSchema()
story_votes_schema = StoryVoteSchema(many=True)
