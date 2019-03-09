from flask_restplus import Namespace, Resource , fields
from models import DirectMessage, Conversation, Notification
from app import create_model

messages_api = Namespace(name='Direct Messages', path='/direct_message')
notifications_api = Namespace(name='Notifications', path='/notifications')


@messages_api.route('/')
class DirectMessages(Resource):
    @messages_api.response(code=200, description='Messages Returned Successfully.', model=[DirectMessage.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.param(name='username', type="str", description='Username for Messages to display', required=True)
    @messages_api.param(name='last_retrieved_message_id. ', type="str", description='Nullable.Normally the request '
                                                                                    'returns the first 20 messages when'
                                                                                    ' null.To retrieve more send the id'
                                                                                    ' of the last message retrieved.',
                        nullable=True)
    def get(self):
        ''' Retrieves a list of Direct Messages '''
        pass

    @messages_api.response(code=201, description='Message Created Successfully.')
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.expect(create_model('Message', model={
        'text': fields.String(description='The content of the message.'),
        'username': fields.String(description='Username ,message was send to.')
    }))
    def post(self):
        """ Creates a New Direct Message. """
        pass


@messages_api.route('/conversations')
class Conversations(Resource):
    @messages_api.response(code=200, description='Conversations Returned Successfully.', model=[Conversation.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.param(name='last_retrieved_conversations_id. ', type="str", description='Nullable.Normally the '
                                                                                          'request returns the first 20'
                                                                                          ' conversations when null.To '
                                                                                          'retrieve more send the id of'
                                                                                          ' the last conversations '
                                                                                          'retrieved.', nullable=True)
    def get(self):
        """ Retrieves a list of Conversations. """
        pass


@notifications_api.route('/')
class Notifications(Resource):
    @notifications_api.response(code=200, description='Notifications Returned Successfully.', model=[Notification.
                                api_model])
    @notifications_api.response(code=401, description='Unauthorized access.')
    @notifications_api.param(name='last_notifications_retrieved_id. ', type="str", description='Nullable.Normally the '
                                                                                               'request returns the '
                                                                                               'first 20 notifications '
                                                                                               'when null.To retrieve'
                                                                                               ' more send the id of '
                                                                                               'the last notifications'
                                                                                               ' retrieved.',
                             nullable=True)
    def get(self):
        """ Retrieves a list of Notifications. """
        pass
