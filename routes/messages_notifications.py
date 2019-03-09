from flask_restplus import Namespace, Resource
from models import DirectMessage,Conversation,Notification
from app import create_model

messages_api = Namespace(name='Direct Messages', path='/direct_message')
notifications_api = Namespace(name='Notifications', path='/notifications')

'''
    Use @messages_api and @notifications_api instead of api
    Replace the following class with your resources
'''


@messages_api.route('/')
class DirectMessages(Resource):
    def get(self):
        pass

    def post(self):
        pass


@messages_api.route('/conversations')
class Conversations(Resource):
    def get(self):
        pass


@notifications_api.route('/')
class Notifications(Resource):
    def get(self):
        pass
