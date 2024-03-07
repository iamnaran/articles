import pdb

from flask import Blueprint, request
from flask_restx import Api, Resource
from marshmallow import ValidationError
from flask import jsonify
from article import bcrypt
from article.models.User import User, UserSchema
from article.models import RevokedToken
from article.api.apicontroller import user_controller, role_controller, slang_comment_controller, post_controller
from article.api.apicontroller import comment_controller, auth_controller, slang_controller

from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

endpoints = Blueprint('endpoints', __name__, url_prefix="/api/v1")

api = Api(endpoints, title="FLASK Articles  Rest API", version="1.0", description="FLASK RESTX API ")

ns = api.namespace("article", description="Articles operations")


# @api.errorhandler
# def default_error_handler():
#     message = 'An unhandled exception occurred.'
#     return {'status': False, 'message': message}, 500


@ns.route("/users")
@api.doc('Users from article')
class Users(Resource):
    """User List"""

    def get(self):
        """List all users"""
        message = 'User list fetched successfully'
        users = user_controller.get_all_users()
        return {'status': True, 'message': message, 'data': users}


@ns.route("/posts")
@api.doc('Post from article')
class Posts(Resource):
    """Post List"""

    def get(self):
        """List all posts"""
        message = 'Post list fetched successfully'
        posts = post_controller.get_all_post()
        return {'status': True, 'message': message, 'data': posts}


@ns.route('/post/<int:post_id>')
@api.doc('Post from article')
class postDetails(Resource):
    """Single posts"""

    def get(self, post_id):
        message = 'Post fetched successfully'
        post = post_controller.get_post_by_id(post_id)
        return {'status': True, 'message': message, 'data': post}

    def delete(self):
        message = 'Post deleted successfully'
        post_controller.get_all_post()
        return {'status': True, 'message': message}


@ns.route("/login")
@api.doc('Login user')
class LoginUser(Resource):

    def get(self):
        return "TODO"

    def post(self):

        try:
            email = request.form['email']
            password = request.form['password']
            status, message, auth_token, user = auth_controller.loginUser(email, password)
            return {'status': status, 'message': message, 'data': user, 'auth_token': auth_token}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@ns.route("/register-user")
@api.doc('Register user')
class RegisterUser(Resource):

    def get(self):
        return "TODO"

    def post(self):

        try:
            result = UserSchema().load(request.form)
            username = result['username']
            email = result['email']
            hash_password = bcrypt.generate_password_hash(result['password']).decode('utf-8')
            status, message, registered_user, auth_token = auth_controller.registerUser(username, email, hash_password)

            if status and registered_user:
                user_id = registered_user['id']
                access_token = create_access_token(identity=user_id)
                refresh_token = create_refresh_token(identity=user_id)
                # user_dict = {'access_token': access_token, 'refresh_token': refresh_token, 'auth_token': auth_token,
                #              'user': registered_user}
                user_dict = {'access_token': access_token, 'refresh_token': refresh_token, 'auth_token': auth_token,
                             'user': registered_user}
                return jsonify({'status': status, 'message': message,
                                'data': user_dict})
            else:
                return jsonify({'status': status, 'message': message})

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@ns.route("/token-refresh")
@api.doc('Token Refresh')
class TokenRefresh(Resource):
    """
    Token Refresh Api
    """

    @jwt_required
    def post(self):
        # Generating new access token
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user)

        return {'access_token': access_token}


@ns.route("/logout")
@api.doc('Logout Api')
class UserLogoutAccess(Resource):
    """
    User Logout Api
    """

    @jwt_required
    def post(self):

        jti = get_jwt()['jti']

        try:
            # Revoking access token
            revoked_token = RevokedToken(jti=jti)

            revoked_token.add()

            return {'status': False, 'message': 'Access token has been revoked'}

        except:

            return {'status': False, 'message': 'Something went wrong'}, 500


@ns.route("/logout-refresh")
@api.doc('Logout Api')
class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api
    """

    @jwt_required
    def post(self):

        jti = get_raw_jwt()['jti']

        try:

            revoked_token = RevokedToken(jti=jti)

            revoked_token.add()

            pdb.set_trace()

            return {'status': False, 'message': 'Refresh token has been revoked'}

        except:

            return {'status': False, 'message': 'Something went wrong'}, 500


@ns.route("/jwt-test", methods=['GET'])
@api.doc('JWT TEST')
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }


@jwt_required
@ns.route("/post/create", methods=['POST'])
@api.doc('Create Post article')
class Posts(Resource):
    """Post List"""

    def post(self):
        """List all posts"""

        try:
            auth_header = request.headers.get('Authorization')
            title = request.form['title']
            content = request.form['content']
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)
            userId = User.decode_auth_token(auth_token=auth_token)
            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        post = post_controller.create_new_post(title=title, content=content, user_id=user.id)
                        if post:
                            message = 'User posted successfully'
                            return {'status': True, 'message': message, 'data': post}

                        else:
                            message = 'Cannot identify user id'
                            return {'status': True, 'message': message, 'data': "cannot post"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user id'
                    return {'status': True, 'message': message}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/post/comment/create", methods=['POST'])
@api.doc('Create Comment for article')
class Comments(Resource):
    """Comment List"""

    def post(self):
        """Post a comment"""

        try:
            auth_header = request.headers.get('Authorization')
            comment_content = request.form['comment']
            post_id_content = request.form['post_id']
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)
            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        comment = comment_controller.post_a_new_comment(comment=comment_content, user_id=user.id,
                                                                        post_id=post_id_content)
                        if comment:
                            message = 'User commented successfully'
                            return {'status': True, 'message': message, 'data': comment}

                        else:
                            message = 'Cannot identify user id'
                            return {'status': True, 'message': message, 'data': "cannot post"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user id'
                    return {'status': True, 'message': message}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/post/<int:post_id>", methods=['GET'])
@api.doc("Get post and comment by post id ")
class GetPostWithComments(Resource):

    def get(self, post_id):

        try:
            auth_header = request.headers.get('Authorization')
            post_id_content = post_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            # return {'status': True, 'message': post_id_content, 'data': userId}

            if userId:
                user = User.find_by_Id(user_id=userId)
                post = post_controller.get_post_by_id(post_id)

                if user and post:
                    try:
                        comments = comment_controller.get_all_comment_by_post(post_id=post_id_content)
                        if comments:
                            message = 'Comments received successfully'

                            response_dict = {'post': post, 'comments': comments}

                            return {'status': True, 'message': message, 'data': response_dict}

                        else:
                            message = 'No Comments'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/post/comments/<int:post_id>", methods=['GET'])
@api.doc("Get all comments by post id ")
class AllComments(Resource):
    def get(self, post_id):

        try:
            auth_header = request.headers.get('Authorization')
            post_id_content = post_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            # return {'status': True, 'message': post_id_content, 'data': userId}

            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        comments = comment_controller.get_all_comment_by_post(post_id=post_id_content)
                        if comments:
                            message = 'Comments received successfully'
                            return {'status': True, 'message': message, 'data': comments}

                        else:
                            message = 'No Comments'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/post/like/<int:post_id>", methods=['POST'])
@api.doc("Like a post , 0=Liked , 1= Unliked ")
class PostLike(Resource):

    def post(self, post_id):

        try:
            auth_header = request.headers.get('Authorization')
            post_id_content = post_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            if userId:
                user = user_controller.get_user_by_id(userId)

                if user:
                    try:
                        post_like = post_controller.post_a_like(post_id=post_id_content,
                                                                user_id=user['id'])
                        if post_like:
                            message = 'Post liked successfully'
                            return {'status': True, 'message': message, 'data': post_like}

                        else:
                            message = 'No Fuck Given'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@ns.route("/create-role", methods=['POST'])
@api.doc('Create Roles for article')
class Comments(Resource):
    """Role Create"""

    def post(self):
        """List all posts"""

        try:
            roleName = request.form['role_name']
            try:
                roles = role_controller.create_new_role(roleName=roleName)
                if roles:
                    message = 'Role Created Successfully'
                    return {'status': True, 'message': message, 'data': roles}

                else:
                    message = 'Cannot add role'
                    return {'status': True, 'message': message, 'data': "cannot add role"}

            except ValidationError as err:
                return {'status': "status", 'message': err.messages}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


# Slang Words
# Working

@jwt_required
@ns.route("/slang/create", methods=['POST'])
@api.doc('Create Slang Word')
class Slangs(Resource):
    """Post List"""

    def post(self):
        """List all posts"""

        try:
            auth_header = request.headers.get('Authorization')
            title = request.form['title']
            content = request.form['content']
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)
            userId = User.decode_auth_token(auth_token=auth_token)
            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        word = slang_controller.create_new_slang_word(title=title, content=content, user_id=user.id)
                        if word:
                            message = 'Word Added successfully'
                            return {'status': True, 'message': message, 'data': word}

                        else:
                            message = 'Cannot identify user id'
                            return {'status': True, 'message': message, 'data': "cannot post"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user id'
                    return {'status': True, 'message': message}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/slang/comment/create", methods=['POST'])
@api.doc('Create Comment for article')
class SlangComments(Resource):
    """Post List"""

    def post(self):
        """List all posts"""

        try:
            auth_header = request.headers.get('Authorization')
            comment_content = request.form['comment']
            word_id_content = request.form['word_id']
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)
            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        comment = slang_comment_controller.post_a_new_comment(comment=comment_content, user_id=user.id,
                                                                              word_id=word_id_content)
                        if comment:
                            message = 'User commented successfully'
                            return {'status': True, 'message': message, 'data': comment}

                        else:
                            message = 'Cannot identify user id'
                            return {'status': True, 'message': message, 'data': "cannot post"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user id'
                    return {'status': True, 'message': message}

        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/slang/<int:word_id>", methods=['GET'])
@api.doc("Get word and comment by word id ")
class GetSlangWithComments(Resource):

    def get(self, word_id):

        try:
            auth_header = request.headers.get('Authorization')
            word_id_content = word_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            # return {'status': True, 'message': post_id_content, 'data': userId}

            if userId:
                user = User.find_by_Id(user_id=userId)
                word = slang_controller.get_slang_by_id(word_id)

                if user and word:
                    try:
                        comments = slang_comment_controller.get_all_comment_by_slang(word_id=word_id_content)
                        if comments:
                            message = 'Post received successfully'

                            response_dict = {'details': word, 'comments': comments}

                            return {'status': True, 'message': message, 'data': response_dict}

                        else:
                            message = 'No Comments'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/slang/comments/<int:post_id>", methods=['GET'])
@api.doc("Get all comments by word id ")
class AllSlangComments(Resource):
    def get(self, post_id):

        try:
            auth_header = request.headers.get('Authorization')
            word_id_content = word_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            # return {'status': True, 'message': post_id_content, 'data': userId}

            if userId:
                user = User.find_by_Id(user_id=userId)

                if user:
                    try:
                        comments = slang_comment_controller.get_all_comment_by_slang(word_id=word_id_content)
                        if comments:
                            message = 'Comments received successfully'
                            return {'status': True, 'message': message, 'data': comments}

                        else:
                            message = 'No Comments'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/slang/upvote/<int:word_id>", methods=['POST'])
@api.doc("Like a slang , 0=Liked , 1= Unliked ")
class SlangUpvote(Resource):

    def post(self, word_id):

        try:
            auth_header = request.headers.get('Authorization')
            word_id_content = word_id
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)

            userId = User.decode_auth_token(auth_token=auth_token)

            if userId:
                user = user_controller.get_user_by_id(userId)

                if user:
                    try:
                        word_upvote = slang_controller.upvote_slang(word_id=word_id_content,
                                                                    user_id=user['id'])
                        if word_upvote:
                            message = 'Word upvote successfully'
                            return {'status': True, 'message': message, 'data': word_upvote}

                        else:
                            message = 'No Fuck Given'
                            return {'status': True, 'message': message, 'data': "null"}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}

                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}


        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


# User Follow & Unfollow

@jwt_required
@ns.route("/follow/<username>", methods=['POST'])
@api.doc("Follow a user")
class Followers(Resource):

    def post(self, username):

        try:
            auth_header = request.headers.get('Authorization')
            username_content = username
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)
            currentUserId = User.decode_auth_token(auth_token=auth_token)

            print("Called current user id", currentUserId)

            if currentUserId:
                user = user_controller.get_user_by_id(currentUserId)

                print(user)
                if user:
                    try:
                        userToFollow = user_controller.get_user_by_username(username=username_content)
                        if userToFollow is None or userToFollow == user:
                            message = 'Username not valid to follow, You gotta be kidding right ??'
                            return {'status': False, 'message': message, 'data': "null"}
                        else:
                            data = user_controller.follow_user(currentUserId, userToFollow['id'])
                            message = 'Followed Successfully'
                            return {'status': True, 'message': message, 'data': data}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}
                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}
        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/unfollow/<username>", methods=['POST'])
@api.doc("UnFollow a user")
class UnFollow(Resource):

    def post(self, username):

        try:
            auth_header = request.headers.get('Authorization')
            username_content = username
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)
            currentUserId = User.decode_auth_token(auth_token=auth_token)

            print("Called current user id", currentUserId)

            if currentUserId:
                user = user_controller.get_user_by_id(currentUserId)

                print(user)
                if user:
                    try:
                        userToFollow = user_controller.get_user_by_username(username=username_content)
                        if userToFollow is None or userToFollow == user:
                            message = 'Username not valid to follow, You gotta be kidding right ??'
                            return {'status': False, 'message': message, 'data': "null"}
                        else:
                            data = user_controller.unfollow_user(currentUserId, userToFollow['id'])
                            message = 'UnFollowed Successfully'
                            return {'status': True, 'message': message, 'data': data}

                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}
                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}
        except ValidationError as err:
            return {'status': "status", 'message': err.messages}


@jwt_required
@ns.route("/get-followers", methods=['POST'])
@api.doc("Get all followers")
class UnFollow(Resource):

    def post(self):

        try:
            auth_header = request.headers.get('Authorization')
            user_id = request.form['user_id']
            auth_token = auth_controller.check_auth_header(auth_header=auth_header)
            currentUserId = User.decode_auth_token(auth_token=auth_token)
            if currentUserId:
                user = user_controller.get_user_by_id(currentUserId)
                if user:
                    try:
                        userFollowers = user_controller.get_all_followers(user_id=user_id)
                        message = 'Called Here'
                        return {'status': False, 'message': message, 'data': userFollowers}


                    except ValidationError as err:
                        return {'status': "status", 'message': err.messages}
                else:
                    message = 'Cannot identify user'
                    return {'status': True, 'message': message}
        except ValidationError as err:
            return {'status': "status", 'message': err.messages}




