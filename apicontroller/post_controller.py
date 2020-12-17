from articles import db
from articles.models.Post import Post
from articles.models.Post import posts_schema, post_schema


def get_all_post():
    all_posts = Post.query.all()
    return posts_schema.dump(all_posts)


def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    return post_schema.dump(post)


def delete_post_by_id(post_id):
    post = Post.query.get(post_id)
    return post_schema.dump(post)


def create_new_post(title, content, user_id):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post)
