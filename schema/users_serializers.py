from articles import api
from flask_restx import fields

user = api.model('User', {
    'user': fields.String(required=True, description='The task details')
})