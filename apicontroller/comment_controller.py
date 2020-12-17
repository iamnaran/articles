from articles import db
from articles.models.Comment import Comment
from articles.models.Comment import commentSchema, commentsSchema


def get_all_comment_by_post(post_id):
    all_comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.commented_date.desc())
    return commentsSchema.dump(all_comments)


def post_a_new_comment(comment, user_id, post_id):
    comment = Comment(comment=comment, user_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return commentSchema.dump(comment)


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

