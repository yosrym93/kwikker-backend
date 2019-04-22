from flask_restplus import Resource, fields, abort, marshal
from flask import request
from models import DirectMessage, Conversation, User
from app import create_model
from . import actions
import api_namespaces
from authentication_and_registration.actions import authorize
from users_profiles import actions as user_profile_actions
from timelines_and_trends import actions as tre_time_actions
from flask_restplus import abort, marshal
from app import socketio
from flask_socketio import send, emit, join_room, leave_room , Namespace

messages_api = api_namespaces.messages_api


@socketio.on('on_retrieve',namespace= '/chat')
@socketio.on_error('/chat')
def on_retrieve(data):
    """
        this function send back a list of direct messages using sockets.
    *Returns*:
        -*Error Response*: if there is an error.
        -*list of DMs*: if everything is ok.
    """
    authorized_username = data['authorized_username']
    to_username = data['to_username']
    last_message_retrieved_id = data ['last_message_retrieved_id']
    #authorized_username = 'ahly'
    #to_username = 'zamalek'
    #last_message_retrieved_id = None
    try:
        messages = actions.get_messages(authorized_username, to_username, last_message_retrieved_id)
        if messages is None:
            abort(404, message='A message with the provided ID does not exist.')
        else:
            if len(messages) == 0:
                emit("receive",[])
            emit("receive",marshal(messages,DirectMessages.api_model))
    except TypeError:
        abort(500, message='An error occurred in the server.')
    except ValueError:
        abort(400, message='Invalid ID provided.')
    except Exception as E:
        if str(E) == 'Username who want to receive this message does not exist.':
            abort(404, message='Username who want to receive this message does not exist.')
        elif str(E) == 'Username who sent this message does not exist.':
            abort(404, message='Username who want to receive this message does not exist.')
    if messages is None:
        abort(404, message='A message with the provided ID does not exist.')


@socketio.on('on_join',namespace='/chat')
@socketio.on_error('/chat')
def on_join(data):
    """
        this function makes user join a certain room
    *param* : data Json object
    *return*: a msg that a user has entered the room
    """
    username = data['username']
    room = username
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('on_leave',namespace= '/chat')
@socketio.on_error('/chat')
def on_leave(data):
    """
        this function makes user join a certain room
    *param* : data Json object
    *return*: a msg that a user has left the room
    """
    username = data['username']
    room = username
    leave_room(room)
    send(username + ' has left the room.', room= room)


@socketio.on('on_create',namespace='/chat')
@socketio.on_error('/chat')
def on_create(data):
    """
    this function makes user create a msg
    """
    authorized_username = data['authorized_username']
    to_username = data['username']
    text = data['text']
    media_url = data['media_url']
    try:
        actions.create_message(authorized_username, to_username, text, media_url)
    except Exception as E:
        if str(E) == 'Username who want to receive this message does not exist.':
            abort(404, message='Username who want to receive this message does not exist.')
        elif str(E) == 'Username who sent this message does not exist.':
            abort(404, message='Username who sent this message does not exist.')
    send({'message': 'message created successfully'})


@messages_api.route('/')
class DirectMessages(Resource):
    @messages_api.response(code=200, description='Messages returned successfully.', model=[DirectMessage.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User or notification_id does not exist.')
    @messages_api.response(code=500, description='An error occurred in the server.')
    @messages_api.param(name='username', type="str",
                        description='Username that received the message.'
                        ''', required=True''')
    @messages_api.param(name='last_message_retrieved_id', type="str",
                        description='Nullable. Normally the request returns the first 20 messages when null. '
                                    'To retrieve more send the id of the last retrieved message.', nullable=True)
    @messages_api.marshal_with(DirectMessage.api_model, as_list=True)
    @messages_api.doc(security='KwikkerKey')
    @authorize
    def get(self,authorized_username):
        """ Retrieves a list of Direct Messages."""
        to_username = request.args.get('username')
        last_message_retrieved_id = request.args.get('last_message_retrieved_id')
        try:
            messages = actions.get_messages(authorized_username, to_username, last_message_retrieved_id)
            if messages is None:
                abort(404, message='A message with the provided ID does not exist.')
            else:
                if len(messages) == 0:
                    return [], 200
                return messages, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except ValueError:
            abort(400, message='Invalid ID provided.')
        except Exception as E:
            if str(E) == 'Username who want to receive this message does not exist.':
                abort(404, message='Username who want to receive this message does not exist.')
            elif str(E) == 'Username who sent this message does not exist.':
                abort(404, message='Username who want to receive this message does not exist.')
        if messages is None:
            abort(404, message='A message with the provided ID does not exist.')

    @messages_api.response(code=201, description='Message created successfully.')
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.expect(create_model('Sent Message', model={
        'text': fields.String(description='The content of the message.'),
        'username': fields.String(description='Username that will receive the message.')
    }))
    @messages_api.doc(security='KwikkerKey')
    #@socketio.on('Receive')
    @authorize
    def post(self, authorized_username):
        """ Creates a New Direct Message.
            Note:  'media_url': fields.String(description='Nullable, url of the media.', nullable = True)
            is in the payload
        """
        data = request.get_json()
        to_username = data['username']
        text = data['text']
        media_url = data['media_url']
        try:
            actions.create_message(authorized_username, to_username, text, media_url)
        except Exception as E:
            if str(E) == 'Username who want to receive this message does not exist.':
                abort(404, message='Username who want to receive this message does not exist.')
            elif str(E) == 'Username who sent this message does not exist.':
                abort(404, message='Username who sent this message does not exist.')
        return {'message': 'message created successfully'}, 200


@messages_api.route('/conversations')
class Conversations(Resource):
    @messages_api.response(code=200, description='Conversations returned successfully.', model=[Conversation.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User or notification_id does not exist.')
    @messages_api.param(name='last_conversations_retrieved_id', type="str", description='Nullable. Normally the '
                                                                                        'request returns the first 20'
                                                                                        ' conversations when null. To'
                                                                                        ' retrieve more send the id '
                                                                                        'of the last retrieved '
                                                                                        'conversation.')
    @messages_api.marshal_with(Conversation.api_model, as_list=True)
    @messages_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of user's ongoing conversations. """
        last_conversations_retrieved_id = request.args.get('last_conversations_retrieved_id')
        try:
            conversations = actions.get_conversations(authorized_username, last_conversations_retrieved_id)
            if conversations is None:
                abort(404, message='A message with the provided ID does not exist.')
            else:
                if len(conversations) == 0:
                    return [], 200
                return conversations, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except ValueError:
            abort(400, message='Invalid ID provided.')
        except Exception as E:
            if str(E) == 'Username who sent this message does not exist.':
                abort(404, message='Username who sent this message does not exist.')
        if conversations is None:
            abort(404, message='A message with the provided ID does not exist.')


@messages_api.route('/recent_conversationers')
class RecentConversationers(Resource):
    @messages_api.response(code=200, description='Conversationers returned successfully.', model=[User.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.param(name='last_conversationers_retrieved_username', type="str",
                        description='Nullable. Normally the request returns the first 20 conversationers when null. '
                                    'To retrieve more send the username of the last retrieved conversationers.')
    @messages_api.marshal_with(User.api_model, as_list=True)
    @messages_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):

        """ Retrieves a list of recent users gone conversations. """
        last_conversationers_retrieved_username = request.args.get('last_conversationers_retrieved_username')
        try:
            recent_conversationers = actions.get_recent_conversationers(authorized_username,
                                                                        last_conversationers_retrieved_username)
            if len(recent_conversationers) == 0:
                return [], 200
            return recent_conversationers, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except Exception as E:
            if str(E) == 'Username who sent this message does not exist.':
                abort(404, message='Username sent this message does not exist.')
            elif str(E) == 'Username does not exist.':
                abort(404, message='Username does not exist.')

    @messages_api.response(code=200, description='Conversationers returned successfully.', model=[User.api_model])
    @messages_api.response(code=401, description='Unauthorized access.')
    @messages_api.response(code=404, description='User does not exist.')
    @messages_api.param(name='last_conversationers_retrieved_username', type="str",
                        description='Nullable. Normally the request returns the first 20 conversationers when null.'
                                    'To retrieve more send the username of the last retrieved conversationers')
    @messages_api.expect(create_model('Search Conversationer', model={
        'search_user': fields.String(description='username to search for.')
    }))
    @messages_api.marshal_with(User.api_model, as_list=True)
    @messages_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Retrieves a list of recent users done using search. """
        data = request.get_json()
        last_conversationers_retrieved_username = request.args.get('last_conversationers_retrieved_username')
        if tre_time_actions.is_user(last_conversationers_retrieved_username)is False \
                and last_conversationers_retrieved_username is not None:
            abort(404, message='Username does not exist.')
        search_user = data["search_user"]
        try:
            conversationers = user_profile_actions.search_user(
                authorized_username, search_user, last_conversationers_retrieved_username)
            if len(conversationers) == 0:
                return [], 200
            return conversationers, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
