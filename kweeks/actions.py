
from datetime import datetime
from models import Kweek, Hashtag, Mention, User
from kweeks.query_factory import add_kweek, delete_main_kweek, retrieve_hashtags, retrieve_mentions, retrieve_replies,\
    retrieve_user, check_following, check_blocked,\
    check_muted, retrieve_kweek, get_user, add_kweek_hashtag, create_mention, create_hashtag, check_existing_hashtag, \
    get_kweek_id, update_hashtag, validate_id, check_kweek_writer, check_kweek_mention, check_kweek_owner, add_rekweek,\
    delete_rekweeks, check_kweek_rekweeker, add_like, delete_like
from notifications.actions import create_notifications



def create_kweek(request, authorized_username):
    """
            Set the data needed to be assigned to the kweek object to later be inserted in the data base


            *Parameters:*
                - *request*: the body of The kweek creation request sent from the user.
                - *authorized_username*: The name of the authorized user who sent the request.


            *Returns:*
               -*Tuple*: {
                            | *bool*: To indicate whether kweek credentials creation was successful or not.,
                            | *message (str)*: To specify the reason of failure if detected.
                            | }
    """
    data = {}
    reply_to = request["reply_to"]
    if reply_to is not None:
        if len(reply_to) == 0 or (reply_to.isspace()):
            return False, 'No reply body found'
        if not reply_to.isdigit():
            return False, 'Not valid id'
        check = validate_id(reply_to)
        if len(check) == 0:
            return False, 'Kweek does not exist '
    text = request['text']
    if len(text) == 0 or (text.isspace()):
        return False, 'No text body found'

    # check if str and have a length of minimum one char and is not fully  white space

    hashtags, mentions = extract_mentions_hashtags(text)  # two lists of objects
    partial_user = get_user(authorized_username)
    if len(partial_user) == 0:
        message = 'The authorized user does not exist in the data base'
        return False, message
    else:
        partial_user = partial_user[0]
    status_dic = {'following': None, 'follows_you': None, 'blocked': None, 'muted': None}
    partial_user.update(status_dic)
    user = User(partial_user)  # user obj
    data['id'] = 0
    data['created_at'] = datetime.utcnow()
    data['username'] = authorized_username
    data['hashtags'] = hashtags  # list of dics
    data['mentions'] = mentions  # list of dics
    data['media_url'] = None
    data['number_of_likes'] = 0
    data['number_of_rekweeks'] = 0
    data['number_of_replies'] = 0
    data['rekweek_info'] = None
    data['liked_by_user'] = False
    data['rekweeked_by_user'] = False
    data['user'] = user
    data.update(request)
    kweek = Kweek(data)
    check, message = insert_kweek(kweek)
    return check, message


def insert_kweek(kweek: Kweek):
    """
            Insert the kweek with its associated data in the data base.


            *Parameters:*
                - *kweek object*: The kweek object to be inserted.

            *Returns:*
                   -*Tuple*: {
                                | *bool*: To indicate whether kweek credentials creation was successful or not.,
                                | *message (str)*: To specify the reason of failure if detected.
                                | }

    """
    add_kweek(kweek)
    kweekid = get_kweek_id()
    print(kweekid)
    kid = kweekid[0]['id']
    for hash_obj in kweek.hashtags:
        test = check_existing_hashtag(hash_obj)
        if not test:  # then it is a new hashtag
            create_hashtag(hash_obj)  # create a new hashtag
            hid = check_existing_hashtag(hash_obj)[0]['id']  # then insert it into kweek-hashtag table
        else:
            hid = test[0]['id']
        add_kweek_hashtag(hid, kid, hash_obj)

    for ment in kweek.mentions:
        existed = check_kweek_mention(kid, ment)[0]['count']
        if existed != 0:
            return False, 'Repeated mention in the same kweek'
        response = create_mention(kid, ment)
        if response is not None:
            return False, 'the user mentioned does not exist in the database'
    return True, 'success'


def extract_mentions_hashtags(text):
    """
            Extract mentions and replies for the given kweek.


            *Parameters:*
                - *text*: The text of the kweek to be inserted .

            *Returns:*
                   -*Tuple*: {
                                | *hashtags (hashtag object )*: The list of kweek hashtags,
                                | *mention (mention object )*: The list of kweek mentions.
                                | }

    """
    hashtags = []
    mentions = []
    size = len(text)
    i = 0
    while i < size:
        hashtag_indices_list = []
        mention_indices_list = []
        if text[i] == '#':
            hashtag_indices_list.append(i)
            for i in range(i + 1, len(text)):
                if i == size:
                    break
                if (i == size - 1 and text[i] == ' ') or text[i] == ' ':
                    hashtag_indices_list.append(i)
                elif i == size - 1:
                    hashtag_indices_list.append(i + 1)
                else:
                    continue
                hashtag_text = text[hashtag_indices_list[0]:hashtag_indices_list[1]]
                hashtag = {'indices': hashtag_indices_list, 'text': hashtag_text, 'id': 0}
                hashtags.append(Hashtag(hashtag))
                break
        if text[i] == '@':
            mention_indices_list.append(i)
            for i in range(i + 1, len(text)):
                if (i == size - 1 and text[i] == ' ') or text[i] == ' ':
                    mention_indices_list.append(i)
                elif i == size - 1:
                    mention_indices_list.append(i + 1)

                else:
                    continue
                mention_username = text[mention_indices_list[0] + 1:(mention_indices_list[1])]
                mention = {'indices': mention_indices_list, 'username': mention_username}
                mentions.append(Mention(mention))
                break
        i += 1

    return hashtags, mentions  # lists of objects
########################################################################################################################


def delete_kweek(kid, authorized_username):
    """
           Delete kweek with its credentials.


           *Parameters:*
               - *kid*: The kweek id to be deleted.
               - *authorized_username(string)*: The user currently logged in.


           *Returns:*
               -*Tuple*: {
                            | *check (bool)*: To indicate whether kweek deletion was successful or not.,
                            | *message (str)*: To specify the reason of failure if detected.
                            | }

    """
    check, message = validate_request(kid)
    if not check:
        return check, message
    check = check_kweek_writer(kid, authorized_username)
    if not check:
        check = check_kweek_owner(kid, authorized_username)
        if not check:
            return False, 'Deletion is not allowed'
    delete_main_kweek(kid)
    update_hashtag()
    return True, None

########################################################################################################################


def validate_request(kid):
    """
           Validate the request parametar.


           *Parameters:*
               - *kid*: The kweek id to be Validate.


           *Returns:*
               -*Tuple*: {
                        | *check (bool)*: To indicate whether kweek is valid or not .,
                        | *message (str)*: To specify  the resaon of error .
                        | }

    """
    try:
        int(kid)
        check = validate_id(kid)
        if len(check) == 0:
            message = 'Kweek is not available'
            return False, message
        else:
            return True, 'success'
    except ValueError:
        return False, 'Invalid data type'


def get_kweek(kid, authorized_username, replies_only):
    """
           Get the requested kweek with its credentials.


           *Parameters:*
               - *kid*: The id of the kweek to be retrieved.
               - *authorized_username(string)*: The user currently logged in.
               - *replies_only (bool)*: To indicate whether the kweek with its replies
                  is to be retrieved or the replies only

           *Returns:*
               -*Tuple*: {
                            | *check (bool)*: To indicate whether kweek credentials creation
                            | was successful or not.,
                            | *message (str)*: To specify the reason of failure if detected.
                            | *kweekobj (kweek object )*: the kweek to be retrieved,
                            | *replies (list of int )*: Ids of  the replies to the retrieved kweek .
                            | }

    """
    check, message = validate_request(kid)
    if not check:
        return check, message, None, None
    replies = retrieve_replies(kid)  # rows of kweek table who is set as a reply to the retrieved kweek (ids)
    if replies_only:
        return True, message, None, replies
    hashtags = retrieve_hashtags(kid)  # rows of hahstag-kweek table (*)
    mentions = retrieve_mentions(kid)  # rows of mention table (*)
    rekweeks = retrieve_user(kid, 3)
    likers = retrieve_user(kid, 2)  # rows of likers table for those who liked the kweek (usernames)
    user = retrieve_user(kid, 1)  # row of user profile table fo the user who wrote the kweek (*)
    hashtags_list = []  # list of hashtag objects
    mentions_list = []  # list of mention objects

    if hashtags:
        for hash_obj in hashtags:
            hid = hash_obj['hashtag_id']
            s_index = hash_obj['starting_index']
            e_index = hash_obj['ending_index']
            indices = [s_index, e_index]
            text = hash_obj['text']
            hash_dic = {'id': hid, 'indices': indices, 'text': text}
            hashtag = Hashtag(hash_dic)
            hashtags_list.append(hashtag)

    if mentions:
        for ment in mentions:
            s_index = ment['starting_index']
            e_index = ment['ending_index']
            indices = [s_index, e_index]
            username = ment['username']
            ment_dic = {'indices': indices, 'username': username}
            mention = Mention(ment_dic)
            mentions_list.append(mention)

    user = user[0]
    extrauser = {}
    me = authorized_username
    check = check_following(me, user['username'])
    if check:
        extrauser['following'] = True
    else:
        extrauser['following'] = False

    check = check_following(user['username'], me)
    if check:
        extrauser['follows_you'] = True
    else:
        extrauser['follows_you'] = False

    check = check_blocked(user['username'], me)
    if check:
        extrauser['blocked'] = True
    else:
        extrauser['blocked'] = False
    check = check_muted(user['username'], me)
    if check:
        extrauser['muted'] = True
    else:
        extrauser['muted'] = False
    extrauser.update(user)

    userobj = User(extrauser)

    if replies:
        num_of_replies = len(replies)
    else:
        num_of_replies = 0

    if likers:
        num_of_likes = len(likers)
        liked_by_user = {'username': me} in likers
    else:
        num_of_likes = 0
        liked_by_user = False

    if rekweeks:
        num_of_rekweeks = len(rekweeks)
        rekweeked_by_user = {'username': me} in rekweeks
    else:
        num_of_rekweeks = 0
        rekweeked_by_user = False

    kweekdic = {'hashtags': hashtags_list, 'mentions': mentions_list, 'number_of_likes': num_of_likes,
                'number_of_rekweeks': num_of_rekweeks, 'number_of_replies': num_of_replies,
                'rekweek_info': None,
                'liked_by_user': liked_by_user, 'rekweeked_by_user': rekweeked_by_user, 'user': userobj}
    kweek = retrieve_kweek(kid)  # a row of kweek table
    kweek = kweek[0]
    kweekdic.update(kweek)
    kweekobj = Kweek(kweekdic)
    return True, message, kweekobj, replies


def get_kweek_with_replies(kid, authorized_username, replies_only):
    """
           Get the credentials of both requested kweek and its replies.


           *Parameters:*
               - *kid*: The id of the kweek to be retrieved.
               - *authorized_username(string)*: The user currently logged in.
               - *replies_only (bool)*: To indicate whether the kweek with its replies
                is to be retrieved or the replies only


           *Returns:*
               -*Tuple*: {
                        | *check (bool)*: To indicate whether kweek credentials creation was
                        | successful or not.,
                        | *message (str)*: To specify the reason of failure if detected.
                        | *kweekobj (kweek object )*: the kweek to be retrieved,
                        | *replies (list of kweek objects )*: replies of the retrieved kweek .
                        | }

    """
    replies_list_obj = []
    check, message, kweekobj, replies_list_dics = get_kweek(kid, authorized_username, replies_only)
    if check:
        if replies_list_dics:
            for reply in replies_list_dics:
                relpy_id = reply['id']
                check_replies, message, k, r = get_kweek(relpy_id, authorized_username, False)
                replies_list_obj.append(k)

    return check, message, kweekobj, replies_list_obj
########################################################################################################################


def create_rekweek(request, authorized_username):
    """
            Insert a rekweek in the data base.


            *Parameters:*
                - *request*: the request which contains the id of th kweek to be rekweeked.

            *Returns:*
                   -*Tuple*: {
                                | *bool*: To indicate whether kweek credentials creation was successful or not.,
                                | *message (str)*: To specify the reason of failure if detected.
                                | }

    """
    rekweek_id = request["id"]
    if id is not None:
        if len(rekweek_id) == 0 or (rekweek_id.isspace()):
            return False, 'No id found'
        if not rekweek_id.isdigit():
            return False, 'Not valid id'
        check = validate_id(rekweek_id)
        if len(check) == 0:
            return False, 'Kweek does not exist '
    else:
        return False, 'No id found'
    partial_user = get_user(authorized_username)
    if len(partial_user) == 0:
        message = 'The authorized user does not exist in the data base'
        return False, message
    add_rekweek(rekweek_id, authorized_username)
    notified_user = retrieve_user(rekweek_id, 1)[0]['username']
    create_notifications(authorized_username, notified_user, 'REKWEEK', rekweek_id)
    return True, 'success '


def delete_rekweek(kweek_id, authorized_username):
    """
           Delete a rekweek .


           *Parameters:*
               - *kweek_id*: The id of the kweek to be deleted.
               - *authorized_username(string)*: The user currently logged in.


           *Returns:*
               -*Tuple*: {
                            | *check (bool)*: To indicate whether kweek deletion was successful or not.,
                            | *message (str)*: To specify the reason of failure if detected.
                            | }

    """
    check, message = validate_request(kweek_id)
    if not check:
        return check, message
    check = check_kweek_rekweeker(kweek_id, authorized_username)
    if not check:
        return False, 'Deletion is not allowed'
    delete_rekweeks(kweek_id)
    return True, 'success '


def like_kweek(request, authorized_username):
    """
            To like a kweek.


            *Parameters:*
                - *request*: Request which contains the id of th kweek to be liked.
                - *authorized_username(string)*: The user currently logged in.

            *Returns:*
                   -*Tuple*: {
                                | *bool*: To indicate whether kweek credentials creation was successful or not.,
                                | *message (str)*: To specify the reason of failure if detected.
                                | }

        """
    kweek_id = request['id']
    if id is not None:
        if len(kweek_id) == 0 or (kweek_id.isspace()):
            return False, 'No id found'
        if not kweek_id.isdigit():
            return False, 'Not valid id'
        check = validate_id(kweek_id)
        if len(check) == 0:
            return False, 'Kweek does not exist '
    else:
        return False, 'No id found'
    add_like(kweek_id, authorized_username)
    notified_user = retrieve_user(kweek_id, 1)[0]['username']
    create_notifications(authorized_username, notified_user, 'LIKE', kweek_id)
    return True, 'success '


def dislike_kweek(kweek_id, authorized_username):
    """
           Dislike a kweek .


           *Parameters:*
               - *kweek_id*: The id of the kweek to be disliked.
               - *authorized_username(string)*: The user currently logged in.


           *Returns:*
               -*Tuple*: {
                            | *check (bool)*: To indicate whether like deletion was successful or not.
                            | *message (str)*: To specify the reason of failure if detected.
                            | }

    """
    check, message = validate_request(kweek_id)
    if not check:
        return check, message
    delete_like(kweek_id, authorized_username)
    return True, None


def get_likers(kweek_id, authorized_username):
    check, message = validate_request(kweek_id)
    if not check:
        print('here0')
        return check, message, None
    likers = retrieve_user(kweek_id, 2)
    if likers:
        print('here1')
        retrieve_users(authorized_username, likers)
    else:
        print('here2')
        return False, 'The kweek has no likers', None


def get_rekweekers(kweek_id, authorized_username):
    check, message = validate_request(kweek_id)
    if not check:
        print('here0')
        return check, message, None
    rekweekers = retrieve_user(kweek_id, 3)
    if rekweekers:
        print('here1')
        print(rekweekers)
        retrieve_users(authorized_username, rekweekers)
    else:
        print('here2')
        return False, 'The kweek has no rekweekers', None


def retrieve_users(authorized_username, user_list):
    users_list = []
    me = authorized_username
    for user in user_list:
        extrauser = {}
        check = check_following(me, user['username'])
        if check:
            extrauser['following'] = True
        else:
            extrauser['following'] = False

        check = check_following(user['username'], me)
        if check:
            extrauser['follows_you'] = True
        else:
            extrauser['follows_you'] = False

        check = check_blocked(user['username'], me)
        if check:
            extrauser['blocked'] = True
        else:
            extrauser['blocked'] = False
        check = check_muted(user['username'], me)
        if check:
            extrauser['muted'] = True
        else:
            extrauser['muted'] = False
        user.update(extrauser)
        userobj = User(user)
        users_list.append(userobj)
    print(users_list)
    return True, 'success', users_list

