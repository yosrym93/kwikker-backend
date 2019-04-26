from . import query_factory
import datetime
from timelines_and_trends import actions
from app import socketio
from flask_restplus import  marshal
from models import DirectMessage, Conversation, User
from media import actions as media_actions


def create_message(from_username, to_username, text, media_id=None):
    """
           This function create a message in the database.


           *Parameter:*

               - *from_username*: user who is send the message .
               - *to_username*: user who is received the message.
               - *text*: body of text.
               - *media_id*: url of the media.

           *Returns:*

               - *None*: if the query was executed successfully.
               - *Exception object*: if there is something wrong, return right exception.
      """
    if actions.is_user(from_username) is False:
        raise Exception('Username who sent this message does not exist.')
    if actions.is_user(to_username) is False:
        raise Exception('Username who want to receive this message does not exist.')
    response = query_factory.create_message(from_username, to_username, datetime.datetime.now(), text,
                                            media_actions.create_url(media_id))
    message=  query_factory.get_messages(from_username,to_username)[0]
    if(from_username<to_username):
        channel=from_username+to_username
    else:
        channel=to_username+from_username
    socketio.emit(channel,marshal(message, DirectMessage.api_model))
    return response


def get_messages(from_username, to_username, last_message_retrieved_id=None):
    """
         This function get list of messages from (from_user)to (to_username) converting lists of dictionaries
         into lists of DirectMessage model, it calls function from query factory that returns lists of
         dictionaries fit DirectMessage model with the given pagination.

         *Parameter:*

             - *from_username*: user who is send the message.
             - *to_username*: user who is received the message.
             - *last_message_retrieved_id*: id of last message retrieved

         *Returns:*

             - *models.Notification object*
    """

    if last_message_retrieved_id is not None:
        try:
            last_message_retrieved_id = int(last_message_retrieved_id)
        except ValueError:
            raise
    if actions.is_user(from_username) is False:
        raise Exception('Username who sent this message does not exist.')
    if actions.is_user(to_username) is False:
        raise Exception('Username who want to receive this message does not exist.')
    messages = query_factory.get_messages(from_username, to_username)
    try:
        messages = actions.paginate(dictionaries_list=messages, required_size=20,
                                    start_after_key='id', start_after_value=last_message_retrieved_id)
    except TypeError:
        raise
    if messages is None:
        return None
    message_list = []
    if len(messages) == 0:
        return message_list
    for message in messages:
        message['created_at'] = change_time(message['created_at'])
        message_list.append(DirectMessage(message))
    return message_list


def get_conversations(auth_username, last_conversations_retrieved_id=None):
    """
         This function get list of conversation between two users converting lists of dictionaries
         into lists of Conversation model, it calls function from query factory that returns lists of
         dictionaries fit Conversation model with the given pagination.

         *Parameter:*

             - *auth_username*: user who is logging in.
             - *last_conversations_retrieved_id*: id of last message retrieved

         *Returns:*

             - *models.Conversation object*
    """

    if last_conversations_retrieved_id is not None:
        try:
            last_conversations_retrieved_id = int(last_conversations_retrieved_id)
        except ValueError:
            raise
    if actions.is_user(auth_username) is False:
        raise Exception('Username who sent this message does not exist.')
    conversations = query_factory.get_conversations(auth_username)
    try:
        conversations = actions.paginate(dictionaries_list=conversations, required_size=20,
                                         start_after_key='id', start_after_value=last_conversations_retrieved_id)
    except TypeError:
        raise
    if conversations is None:
        return None

    conversation_list = []
    if len(conversations) == 0:
        return conversation_list
    for conversation in conversations:
        to_username = conversation['to_username']
        from_username = conversation['from_username']
        dictionary = {'id': conversation['id']}
        temp = {'from_username':from_username}
        dictionary.update(temp)
        temp = {'to_username': to_username}
        dictionary.update(temp)
        new_format = change_time(conversation['created_at'])
        temp = {'created_at': new_format}
        dictionary.update(temp)
        temp = {'text': conversation['text']}
        dictionary.update(temp)
        temp = {'media_url': conversation['media_url']}
        dictionary.update(temp)
        direct_message = DirectMessage(dictionary)
        dic = {'last_message': direct_message}
        if to_username == auth_username :
            username = from_username
        else:
            username = to_username
        dictionary = {'username': username}
        temp = {'screen_name': conversation['screen_name']}
        dictionary.update(temp)
        temp = {'profile_image_url': conversation['profile_image_url']}
        dictionary.update(temp)
        flag = check_follow(auth_username, username)
        temp = {'following': flag}
        dictionary.update(temp)
        flag = check_follow(username, auth_username)
        temp = {'follows_you': flag}
        dictionary.update(temp)
        flag = check_block(auth_username, username)
        temp = {'blocked': flag}
        dictionary.update(temp)
        flag = check_mute(auth_username, username)
        temp = {'muted': flag}
        dictionary.update(temp)
        user = User(dictionary)
        dic2 = {'user': user}
        dic2.update(dic)
        conversation_list.append(Conversation(dic2).to_json())
    return conversation_list


def check_follow(follower, followed):
    """
            This function checks if the user follows another user in the database or not.


            *Parameter:*

                - *follower:* follower user to be checked in the database.
                - *followed:* followed user to be checked in the database.

            *Returns:*
                - a query to be check if exist or not.
    """
    return query_factory.check_follow(follower, followed)


def check_block(blocker, blocked):
    """
              This function checks if the user blocked another user in the database or not.


              *Parameter:*

                  - *blocker:* blocker user to be checked in the database.
                  - *blocked:* blocked user to be checked in the database.

              *Returns:*
                  - a query to be check if exist or not.
      """
    return query_factory.check_block(blocker, blocked)


def check_mute(muter, muted):
    """
            This function checks if the user muted another user in the database or not.


            *Parameter:*

                - *muter:* muter user to be checked in the database.
                - *muted:* muted user to be checked in the database.

            *Returns:*
                - a query to be check if exist or not.
    """
    return query_factory.check_mute(muter, muted)


def change_time(day_time):
    """
            This function format of time  .


            *Parameter:*

                - *day_time:* time to be changed in the database.

            *Returns:*
                - return time with the required format.
    """
    now = datetime.datetime.now()
    difference = now - day_time
    if difference.days > 0:
        if now.year == day_time.year:
            new_format = day_time.strftime("%B %d")
        else:
            new_format = day_time.strftime("%B %d,%Y")
    else:
        if int(difference.seconds) < 60:
            new_format = str(difference.seconds) + 's'
        elif int(difference.seconds) > 3600:
            new_format = str(int(difference.seconds) // 3600) + 'h'
        else:
            new_format = str(int(difference.seconds) // 60) + 'm'
    return new_format


def get_recent_conversationers(from_username, last_conversationers_retrieved_username=None):
    """
         This function get list of conversationers between two users converting lists of dictionaries
         into lists of Conversation model, it calls function from query factory that returns lists of
         dictionaries fit Conversation model with the given pagination.

         *Parameter:*

             - *from_username*: user who is send the message.
             - *last_conversationers_retrieved_username*: id of last message retrieved

         *Returns:*

             - *models.User object*
    """
    if actions.is_user(from_username) is False:
        raise Exception('Username who sent this message does not exist.')
    if last_conversationers_retrieved_username is not None:
        if actions.is_user(last_conversationers_retrieved_username) is False:
            raise Exception('Username does not exist.')
    conversationers = query_factory.get_recent_conversationers(from_username)
    try:
        conversationers = actions.paginate(dictionaries_list=conversationers, required_size=20,
                                           start_after_key='username',
                                           start_after_value=last_conversationers_retrieved_username)
    except TypeError:
        raise
    if conversationers is None:
        return []
    conversationer_list = []
    if len(conversationers) == 0:
        return conversationer_list
    for conversation in conversationers:
        to_username = conversation['username']

        dictionary = {'username': to_username}
        temp = {'screen_name': conversation['screen_name']}
        dictionary.update(temp)
        temp = {'profile_image_url': conversation['profile_image_url']}
        dictionary.update(temp)
        flag = check_follow(from_username, to_username)
        temp = {'following': flag}
        dictionary.update(temp)
        flag = check_follow(to_username, from_username)
        temp = {'follows_you': flag}
        dictionary.update(temp)
        flag = check_block(from_username, to_username)
        temp = {'blocked': flag}
        dictionary.update(temp)
        flag = check_mute(from_username, to_username)
        temp = {'muted': flag}
        dictionary.update(temp)
        user = User(dictionary)

        conversationer_list.append(user)
    return conversationer_list
