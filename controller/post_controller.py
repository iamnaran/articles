from articles.schema.post_schema import posts_schema
from articles.models import Post


def get_all_post():
    all_posts = Post.query.all()
    return posts_schema.dump(all_posts)
