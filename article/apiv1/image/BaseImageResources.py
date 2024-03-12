from flask import request
from flask_restx import Resource, Namespace
from article import db
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app
from flask import send_from_directory

import cv2
import numpy as np
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
    
    @staticmethod
    def optimize_base64_image(base64_data):
        # Decode base64 data
        image_data = base64.b64decode(base64_data)
        
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)        
        max_width = 800
        if image.shape[1] > max_width:
            aspect_ratio = max_width / image.shape[1]
            new_height = int(image.shape[0] * aspect_ratio)
            image = cv2.resize(image, (max_width, new_height), interpolation=cv2.INTER_AREA)
        
        _, encoded_image = cv2.imencode('.jpg', image)
        optimized_base64_data = base64.b64encode(encoded_image).decode('utf-8')
        
        return optimized_base64_data


    def post(self):
        try:
            if 'image' not in request.files:
                return {'message': 'No file part'}, 400

            file = request.files['image']
            if file.filename == '':
                return {'message': 'No selected file'}, 400
            
            if file and self.allowed_file(file.filename):
                base64_data = base64.b64encode(file.read()).decode('utf-8')
                optimized_base64_data = self.optimize_base64_image(base64_data)
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





  
   

