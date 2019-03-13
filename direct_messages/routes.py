from flask_restplus import Resource, fields
from models import DirectMessage, Conversation
from app import create_model
from api_namespaces import APINamespaces

messages_api = APINamespaces.messages_api


@messages_api.route('/')
class DirectMessages(Resource):
    @messages_api.response(code=200, description='Messages returned successfully.', model=[DirectMessage.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.param(name='username', type="str",
                        description='The username of the user whose conversation messages are to be retrieved.',
                        required=True)
    @messages_api.param(name='last_retrieved_message_id. ', type="str", description='Nullable. Normally the request '
                                                                                    'returns the first 20 messages when'
                                                                                    ' null. To retrieve more send the '
                                                                                    'id of the last retrieved message.',
                        nullable=True)
    def get(self):
        """ Retrieves a list of Direct Messages. """
        pass

    @messages_api.response(code=201, description='Message created successfully.')
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.expect(create_model('Sent Message', model={
        'text': fields.String(description='The content of the message.'),
        'username': fields.String(description='Username of the user that the message was sent to.')
    }))
    def post(self):
        """ Creates a New Direct Message. """
        pass


@messages_api.route('/conversations')
class Conversations(Resource):
    @messages_api.response(code=200, description='Conversations returned successfully.', model=[Conversation.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.param(name='last_retrieved_conversations_id. ', type="str", description='Nullable. Normally the '
                                                                                          'request returns the first 20'
                                                                                          ' conversations when null. To'
                                                                                          ' retrieve more send the id '
                                                                                          'of the last retrieved '
                                                                                          'conversation.')
    def get(self):
        """ Retrieves a list of user's ongoing conversations. """
        pass
