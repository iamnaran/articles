from datetime import datetime
from articles import ma
from marshmallow import fields, validate

from articles import db


class EventGallery(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    photos = db.Column(db.Text, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # return f"User('{self.comment}','{self.commented_date}','{self.user_id}','{self.post_id}')"
        return ""


class EventGallerySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = EventGallery
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    photos = fields.String(required=True)
    event_id = fields.String(required=True)
    created_at = fields.DateTime(required=True)


eventGallerySchema = EventGallerySchema()
eventsGallerySchema = EventGallerySchema(many=True)
