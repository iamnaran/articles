import datetime
from article import ma
from marshmallow import fields, validate
from article.models.StoryComment import StoryComment, StoryCommentSchema
from article.models.StoryFile import StoryFileSchema
from article.models.StoryVote import StoryVote, StoryVoteSchema

from article import db


class Story(db.Model):
    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    tags = db.Column(db.Text, nullable=False)
    files = db.relationship('StoryFile', backref='files', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('StoryComment', backref='comments', lazy=True)
    votes = db.relationship('StoryVote', backref='votes', lazy=True)

    def __repr__(self):
        return f"Article('{self.title}','{self.content}','{self.created_at}')"

    @staticmethod
    def get_all_stories():
        stories = Story.query.all()
        return stories_schema.dump(stories)

    @staticmethod
    def get_story_by_id(story_id):
        story = Story.query.get(story_id)
        return story_schema.dump(story)


class StorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Story
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, help='Title required.')
    sub_title = fields.String(required=True, help='Sub title required.')
    content = fields.String(required=True, help='Content required')
    tags = fields.String(required=True, help='Tags required')
    photos = fields.String(required=True, help='Photos required')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    files = fields.Nested(StoryFileSchema, many=True)
    author = fields.Nested("UserSchema", only=("id", "username", "email",), many=False)
    comments = fields.Nested(StoryCommentSchema, many=True)
    votes = fields.Nested(StoryVoteSchema, many=True)


story_schema = StorySchema()
stories_schema = StorySchema(many=True)
