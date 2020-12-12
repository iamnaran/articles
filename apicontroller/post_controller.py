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
