from articles.models import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = User


user_schema = UserSchema()
users_schema = UserSchema(many=True)
