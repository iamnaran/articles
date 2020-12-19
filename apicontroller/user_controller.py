from articles.models.User import User
from articles.models.User import users_schema, user_schema


def get_all_users():
    all_users = User.query.all()
    return users_schema.dump(all_users)


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user_schema.dump(user)
