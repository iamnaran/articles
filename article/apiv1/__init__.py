from flask_restx import Api
from flask import Blueprint

from article.apiv1.post.PostResources import post_apis
from article.apiv1.post.PostOperationResources import post_operation_apis
from article.apiv1.post.CommentResources import comment_apis
from article.apiv1.post.CommentOpResources import comment_operation_apis
from article.apiv1.post.LikeResources import likeapis

from article.apiv1.auth.LoginResource import auth_apis
from article.apiv1.auth.RegisterResource import auth_register_apis
from article.apiv1.users.FollowResource import follow_apis
from article.apiv1.users.ProfileResource import profile_apis



from article.apiv1.StoryResources import stories_apis
from article.apiv1.home.HomeResource import homePageApis






apis = Blueprint('apis', __name__, url_prefix='/api/v1')

api = Api(apis,
          title='Articles',
          version='1.0',
          description='A Article project',
          )

api.add_namespace(post_apis, path='/userpost')
api.add_namespace(post_operation_apis, path='/userpost')
api.add_namespace(profile_apis, path='/profile')
api.add_namespace(comment_apis, path='/comments')
api.add_namespace(comment_operation_apis, path='/comments')
api.add_namespace(likeapis, path='/likes')


api.add_namespace(auth_apis, path='/auth')
api.add_namespace(auth_register_apis, path='/auth')
api.add_namespace(follow_apis, path='/follow')

api.add_namespace(homePageApis, path='/home')
api.add_namespace(stories_apis, path='/stories')
