from articles.models.User import User
from articles.models.User import users_schema, user_schema


def get_all_users():
    all_users = User.query.all()
    return users_schema.dump(all_users)


