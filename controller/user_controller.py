from articles.models.model_user import User
from articles.models.model_user import users_schema, user_schema


def get_all_users():
    all_users = User.query.all()
    return users_schema.dump(all_users)
