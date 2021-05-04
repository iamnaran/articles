from article import db
from article.models.Event import Event
from article.models.Event import eventSchema, eventsSchema


def get_all_events():
    all_events = Event.query.all()
    return eventsSchema.dump(all_events)


def post_a_new_event(title, subtitle, description, start_date, end_date ,  user_id, post_id):
    event = Event(event_title=title, user_id=user_id, post_id=post_id)
    db.session.add(event)
    db.session.commit()
    return eventsSchema.dump(event)


def edit_a_comment(comment, user_id, post_id):
    comment = Comment(comment=comment, user_id=user_id, post_id=post_id)

    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)


def delete_a_comment(comment, user_id, post_id):
    comment = Comment(comment=comment, user_id=user_id, post_id=post_id)

    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)
