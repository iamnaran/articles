from flask import request
from flask.json import jsonify
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from article import db
import traceback
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

class Chatter:
    model_name = "facebook/blenderbot-400M-distill"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    conversation_history = []

    @classmethod
    def process_message(cls, inputMessage):
        try:
            # Create conversation history string
            history_string = "\n".join(cls.conversation_history)
            inputs = cls.tokenizer.encode_plus(history_string, inputMessage, return_tensors="pt")
            outputs = cls.model.generate(**inputs, max_length=60)
            response = cls.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            cls.conversation_history.append(inputMessage)
            cls.conversation_history.append(response)
            return response
        except Exception as e:
            traceback.print_exc()
            return f'Error occurred: {str(e)}'


chatBotApi = Namespace('chatBotApi', description='Home Page Api')
@chatBotApi.route('/bot')
@chatBotApi.doc('Get Home Page Data')
class ChatBotResource(Resource):
    """Chat Bot Apis"""
    
    @cross_origin()
    @jwt_required()
    def post(self):
        """Chat Bot Api"""
        try:
            verify_jwt_in_request()
            inputMessage = request.form['message']
            response = Chatter.process_message(inputMessage)
            message = 'Bot replied'
            return {'status': True, 'message': message, 'input': inputMessage, 'response':response}
        except Exception as e:
            traceback.print_exc()
            message = f'Error occurred: {str(e)}'
            return {'status': False, 'message': message}