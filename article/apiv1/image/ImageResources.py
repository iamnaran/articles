from flask import request
from flask_restx import Resource, Namespace
from article import db
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import send_from_directory


from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

images_apis = Namespace('images_apis', description='File related operations')

@images_apis.route('/upload')
@images_apis.doc('Get all post & Create New Post')
class ImageResource(Resource):
    """Get & Post Images"""

    def get(self, filename):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        try:
            verify_jwt_in_request()
            path = os.getcwd()
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])
            upload_folder = os.path.join(path, current_app.config['UPLOAD_FOLDER'])
            success = False
            file = request.files['image']
           
            if not os.path.isdir(upload_folder):
                os.mkdir(upload_folder)

            if file.filename == '':
                return {'message': 'No selected file'}, 400
            
            if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                filename = some_string = str(uuid.uuid4())+ secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                message = 'Files uploading success'
                return {'status': True, 'message': message, 'data': file_path}, 200
            else:
                message = 'Files uploading failed. Please check your file extension or size of file'
                return {'status': True, 'message': message, 'data': "null"}, 400

        except Exception as err:
            message = 'Some error occurred. '
            return {'status': False, 'message': message + str(err.args), 'data': "null"}



  
   

