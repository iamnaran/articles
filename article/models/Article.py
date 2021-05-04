from datetime import datetime
from article import ma
from marshmallow import fields, validate
from article.models.Comment import CommentSchema

from article import db
from article.models.PostLike import PostLikeSchema


class Article(db.Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sub_title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('PostLike', backref='likes', lazy=True)

    def __repr__(self):
        return f"Article('{self.title}','{self.content}','{self.created_at}')"

    @staticmethod
    def get_all_articles():
        articles = Article.query.all()
        return articles_schema.dump(articles)

    @staticmethod
    def get_article_by_id(post_id):
        post = Article.query.get(post_id)
        return article_schema.dump(post)


class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose
        model = Article
        include_relationships = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, help='Title required.')
    sub_title = fields.String(required=True, help='Sub title required.')
    content = fields.String(required=True, help='Content required')
    tags = fields.String(required=True, help='Tags required')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    author = fields.Nested("UserSchema", only=("id", "username", "email",), many=False)
    comments = fields.Nested(CommentSchema, many=True)
    likes = fields.Nested(PostLikeSchema, many=True)


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
