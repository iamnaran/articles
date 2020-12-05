from articles.models import Post
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Post
        include_relationships = True
        load_instance = True


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
