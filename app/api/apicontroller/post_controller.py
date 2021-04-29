from app import db
from app.models.Post import Post
from app.models.Post import posts_schema, post_schema
from app.models.PostLike import PostLike, post_like_schema


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


def post_a_like(post_id, user_id):
    print(post_id)
    print(user_id)
    try:
        post = PostLike.query.filter_by(post_id=post_id).filter_by(user_id=user_id).first()

        print(post)

        if post:
            if post.is_liked:
                post.is_liked = False
                db.session.commit()
            else:
                post.is_liked = True
                db.session.commit()

            return post_like_schema.dump(post)

        else:
            post_like = PostLike(is_liked=True, post_id=post_id, user_id=user_id)
            db.session.add(post_like)
            db.session.commit()
            return post_like_schema.dump(post_like)

    except Exception as e:
        return False, e.args, "null", "null"
