from datetime import datetime
from article import ma
from marshmallow import fields, validate
from article.models.EventGallery import eventGallerySchema, eventsGallerySchema

from article import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    sub_title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    featured_image = fields.String(required=True)
    gallery = db.relationship('EventGallery', backref='gallery', lazy=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        # return f"User('{self.comment}','{self.commented_date}','{self.user_id}','{self.post_id}')"
        return ""


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Event
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    sub_title = fields.String(required=True)
    description = fields.String(required=True)
    start_date = fields.String(required=True)
    end_date = fields.String(required=True)
    featured_image = fields.String(required=True)
    photos = fields.String(required=False)
    gallery = fields.Nested("EventGallerySchema", only=("id", "photos"))
    created_by = fields.Nested("UserSchema", only=("id", "username", "email"))
    created_at = fields.DateTime(required=True)


eventSchema = EventSchema()
eventsSchema = EventSchema(many=True)
