from articles.models import User
from articles.schema.users_schema import users_schema


def get_all_users():
    all_users = User.query.all()
    return users_schema.dump(all_users)
