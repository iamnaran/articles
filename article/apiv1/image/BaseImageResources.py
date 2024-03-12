from flask import request
from flask_restx import Resource, Namespace
from article import db
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import send_from_directory

import base64

from article.models.image.BaseImage import BaseImage, baseImageSchema, baseImagesSchema


from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

base64_images_apis = Namespace('base64_images_apis', description='File related operations')

@base64_images_apis.route('/upload')
@base64_images_apis.doc('Upload Images')
class ImageResource(Resource):
    """Add Base 64  Images"""

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

    def post(self):
        try:
            if 'image' not in request.files:
                return {'message': 'No file part'}, 400

            file = request.files['image']
            if file.filename == '':
                return {'message': 'No selected file'}, 400
            
            if file and self.allowed_file(file.filename):
                optimized_base64_data = base64.b64encode(file.read()).decode('utf-8')
                filename = str(uuid.uuid4()) + '.jpg'
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # Save to database
                image_data = BaseImage(filename=filename, base64_data=optimized_base64_data)
                db.session.add(image_data)
                db.session.commit()

                return {'status': True, 'message': 'File uploaded successfully', 'data': baseImageSchema.dump(image_data)}, 200
            else:
                return {'status': False, 'message': 'File upload failed. Please check file extension.'}, 400
        except Exception as e:
            return {'status': False, 'message': str(e)}, 500





  
   

