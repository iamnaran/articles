from flask import request, jsonify
from flask_restx import Resource, Namespace
from article import db, config
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app

from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from article.models.story.StoryFile import StoryFile, story_file_Schema, story_files_schema
from article.models.story.Story import Story, story_schema, stories_schema

stories_apis = Namespace('stories_apis', description='Story related operations')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@stories_apis.route('/story')
@stories_apis.doc('Get all stories & Create New story')
class StoryResources(Resource):
    """Story Create & List"""

    def get(self):
        """List all stories"""
        all_stories = {'all_stories': Story.get_all_stories()}
        print("called")
        print(all_stories)
        message = 'Stories list fetched successfully'
        return {'status': True, 'message': message, 'data': all_stories}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        """Create new story """
        try:
            verify_jwt_in_request()
            title = request.form['title']
            sub_title = request.form['sub_title']
            content = request.form['content']
            tags = request.form['tags']
            errors = {}
            success = False
            path = os.getcwd()
            upload_folder = os.path.join(path, current_app.config['UPLOAD_FOLDER'])

            if 'files[]' not in request.files:
                message = 'Please add your post images to continue. '
                return {'status': success, 'message': message, 'data': "null"}

            if not os.path.isdir(upload_folder):
                os.mkdir(upload_folder)

            if title or sub_title or content or tags is None:
                files = request.files.getlist('files[]')
                story = Story(title=title, sub_title=sub_title, content=content, tags=tags,
                              user_id=get_jwt_identity())
                for file in files:
                    if file and self.allowed_file(file.filename):
                        some_string = str(uuid.uuid4())
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(upload_folder, some_string + filename))
                        story.files.append(
                            StoryFile(file_path=some_string + filename, user_id=get_jwt_identity(), story_id=story.id))
                        success = True
                    else:
                        errors[file.filename] = 'File type is not allowed. '
                if success and errors:
                    message = 'File(s) successfully uploaded with some errors. Please check  your files extension'
                    return {'status': True, 'message': message, 'data': story_schema.dump(story)}
                if success:
                    print(story)
                    db.session.add(story)
                    db.session.commit()
                    message = 'File(s) successfully uploaded. '
                    return {'status': True, 'message': message, 'data': "null"}
                else:
                    message = 'Files uploading failed. Please check your file extension or size of file'
                    return {'status': True, 'message': message, 'data': "null"}

            else:
                message = 'All fields are required.'
                return {'status': True, 'message': message, 'errors': jsonify(errors)}

        except Exception as err:
            message = 'Some error occurred. '
            return {'status': False, 'message': message + err.args[0]}

# try:
#                post = Post(title=title, content=content, user_id=get_jwt_identity())
#                db.session.add(post)
#                db.session.commit()
#                # post = post_controller.create_new_post(title=title, content=content, user_id=get_jwt_identity())
#                if post:
#                    message = 'Posted successfully'
#                    return {'status': True, 'message': message, 'data': post_schema.dump(post)}
#                else:
#                    message = 'Cannot Post'
#                    return {'status': True, 'message': message, 'data': "null"}
#            except:
#                message = 'Error has occurred while posting'
#                return {'status': True, 'message': message, 'data': "null"}
