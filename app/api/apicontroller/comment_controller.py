from app import db
from app.models.SlangComment import SlangComment
from app.models.SlangComment import commentSchema, commentsSchema


def get_all_comment_by_post(post_id):
    all_comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.commented_date.desc())
    return commentsSchema.dump(all_comments)


def post_a_new_comment(comment, user_id, word_id):
    comment = SlangComment(comment=comment, user_id=user_id, word_id=word_id)
    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)


def edit_a_comment(comment, user_id, word_id):
    comment = SlangComment(comment=comment, user_id=user_id, word_id=word_id)

    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)


def delete_a_comment(comment, user_id, word_id):
    comment = SlangComment(comment=comment, user_id=user_id, word_id=word_id)
    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)

