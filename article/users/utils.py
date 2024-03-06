import os
import secrets
from functools import wraps

from flask_mail import Message
# from PIL import Image
from flask import jsonify, url_for, current_app, request
import jwt
from article import mail
from article.models.User import User


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)
    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='smartgov.article@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'A valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator
