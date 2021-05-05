from article import db
from article.models.User import User
from article.models.User import users_schema, user_schema, UserSchema


def get_all_users():
    all_users = User.query.all()
    return users_schema.dump(all_users)


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user_schema.dump(user)


def get_user_by_username(username):
    user = User.find_by_username(username=username)
    data_schema = UserSchema(only=("id", "username", "email"))
    result = data_schema.dump(user)
    return result


def follow_user(user_id, userToFollowId):
    user = User.find_by_Id(user_id)
    userToFollow = User.find_by_Id(userToFollowId)

    print("called current user ", user)
    print("called user to follow ", userToFollow)

    user.follow(user, userToFollow)
    db.session.commit()
    return user_schema.dump(userToFollow)


def unfollow_user(user_id, userToFollowId):
    user = User.find_by_Id(user_id)
    userToFollow = User.find_by_Id(userToFollowId)
    print("called current user ", user)
    print("called user to unfollow ", userToFollow)
    user.un_follow(user, userToFollow)
    db.session.commit()
    return user_schema.dump(userToFollow)


def get_all_followers(user_id):
    user = User.find_by_Id(user_id)
    print(user.followed.all())
    print("Called")
    return ""
