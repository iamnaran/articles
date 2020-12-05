from articles.models.model_post import Post
from articles.models.model_post import posts_schema, post_schema


def get_all_post():
    all_posts = Post.query.all()
    return posts_schema.dump(all_posts)
