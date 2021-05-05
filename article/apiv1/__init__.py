from flask_restx import Api
from flask import Blueprint
from article.apiv1.PostResources import post_apis
from article.apiv1.LoginResource import auth_apis
from article.apiv1.RegisterResource import auth_register_apis
from article.apiv1.StoryResources import stories_apis

apis = Blueprint('apis', __name__, url_prefix='/api/v1')

api = Api(apis,
          title='Articles',
          version='1.0',
          description='A Article project',
          )

api.add_namespace(post_apis, path='/users')
api.add_namespace(auth_apis, path='/auth')
api.add_namespace(auth_register_apis, path='/auth')
api.add_namespace(stories_apis, path='/stories')
