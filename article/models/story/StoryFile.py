from datetime import datetime
from article import ma
from marshmallow import fields, validate

from article import db


class StoryFile(db.Model):
    __tablename__ = 'story-file'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)

    def __init__(self, file_path, user_id, story_id):
        self.file_path = file_path
        self.user_id = user_id
        self.story_id = story_id

    def __repr__(self):
        return f"User('{self.file_path}','{self.created_at}','{self.user_id}','{self.story_id}')"


class StoryFileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = StoryFile
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    file_path = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    story_id = fields.Integer()


story_file_Schema = StoryFileSchema()
story_files_schema = StoryFileSchema(many=True)
