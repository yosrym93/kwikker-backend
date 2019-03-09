from flask_restplus import Namespace, Resource , fields
from models import DirectMessage, Conversation, Notification
from app import create_model

messages_api = Namespace(name='Direct Messages', path='/direct_message')
notifications_api = Namespace(name='Notifications', path='/notifications')


@messages_api.route('/')
class DirectMessages(Resource):
    @messages_api.response(code=200, description='Messages Returned Successfully.', model=[DirectMessage.api_model])
    @messages_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.param(name='Username', type="String", description='Username for Messages to display', required=True)
    @messages_api.param(name='Last_Message_Retrieved. ', type="String", description='Id of the last message retrieved '
                                                                                   ',generally 20 messages are sent if'
                                                                                   ' null ,but can retrieve more by '
                                                                                   'sending id of the last message.'
                                                                                   '', nullable=True)
    def get(self):
        ''' Retrieves a list of Direct Messages '''
        pass

    @messages_api.response(code=201, description='Message Created Successfully.', model=[DirectMessage.api_model])
    @messages_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.expect(create_model('Message', model={
        'Text': fields.String(description='The content of the message.'),
        'Username': fields.String(description='Username ,message was send to.')
    }))
    def post(self):
        ''' Creates a New Direct Message. '''
        pass


@messages_api.route('/conversations')
class Conversations(Resource):
    @messages_api.response(code=200, description='Conversations Returned Successfully.', model=[Conversation.api_model])
    @messages_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    def get(self):
        ''' Retrieves a list of Conversations. '''
        pass


@notifications_api.route('/')
class Notifications(Resource):
    @notifications_api.response(code=200, description='Notifications Returned Successfully.', model=[Notification.
                                api_model])
    @notifications_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    def get(self):
        ''' Retrieves a list of Notifications. '''
        pass
