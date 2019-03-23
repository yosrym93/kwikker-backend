
from datetime import datetime
from models import Kweek, Hashtag, Mention, User, RekweekInfo
from kweeks.query_factory import add_kweek\
    , delete_rekweeks, delete_likes, delete_main_kweek, retrieve_hashtags\
    , retrieve_mentions, retrieve_replies, retrieve_rekweeks, retrieve_user, retrieve_likers, retrieve_hashtag_text\
    , check_following, check_blocked, check_muted, retrieve_kweek, get_user, add_kweek_hashtag, creat_mention\
    , create_hashtag, check_existing_hashtag, get_kweek_id, update_hashtag, validate_id


def create_kweek(request, authorized_username):
    """
                Set the data needed to be assigned to the kweek object to later be inserted in the data base


                *Parameters:*
                    - *request*: the body of The kweek creation request sent from the user.
                    - *authorized_username*: The name of the authorized user who sent the request.


                *Returns:*
                   - *bool*: To indicate whether kweek credentials creation was successful or not.
                   - *message*: To specify the reason of failure if detected.
         """
    data = {}
    check = True
    text = request['text']
    if type(text) != str:
        return False, 'invalid data type '
    if len(text) == 0 or (text.isspace()):
        return False, 'No text body found'

    # check if str and have a length of minimum one char and is not fully  white space
    reply_to = request["reply_to"]
    if reply_to is not None:  # if it was a reply
        if type(reply_to) != int:
            return False, 'invalid data type '
        check = validate_id(reply_to)
        if len(check) == 0:
            return False, 'Kweek does not exist '

    hashtags, mentions = extract_mentions_hashtags(text)  # two lists of objects
    userr = get_user(authorized_username)
    if len(userr) == 0:
        message = 'The user does not exist'
        return False, message
    else:
        userr = userr[0]
    dic = {'following': None, 'follows_you': None, 'blocked': None, 'muted': None}
    userr.update(dic)
    user = User(userr)  # user obj
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
    print(kweek)
    check, message = insert_kweek(kweek)
    return check, message


def insert_kweek(kweek: Kweek):
    """
            Insert the kweek with its associated data in the data base.


            *Parameters:*
                - *kweek object*: The kweek object to be inserted.

            *Returns:*
                - *bool*: To indicate whether the insertion was successful or not.
                - *message*: To specify the reason of failure if detected.
     """
    check = 1
    add_kweek(kweek)
    kid = get_kweek_id(kweek)
    for hash in kweek.hashtags:
        test = check_existing_hashtag(hash)
        if not test:  # then it is a new hashtag
            create_hashtag(hash)  # create a new hashtag
            id = check_existing_hashtag(hash)  # then insert it into kweek-hashtag table
            hid = id[0]['id']
        else:
            hid = test[0]['id']
        kid = kid[0]['id']
        add_kweek_hashtag(hid, kid, hash)

    for ment in kweek.mentions:
        creat_mention(kid, ment)
    message ='every thing went fine'  # then to be replaced
    return True, message


def extract_mentions_hashtags(text):
    """
            Extract mentions and replies for the given kweek.


            *Parameters:*
                - *text*: The text of the kweek to be inserted .

            *Returns:*
                - *List*: The hashtags found within the kweek
                - *List*: The mentions found within the kweek

    """
    hashtags = []
    mentions = []
    size = len(text)
    i = 0
    while i < size:
        hashtag = {}
        mention = {}
        hashtag['indices'] = []
        mention['indices'] = []
        if text[i] == '#':
            hashtag['indices'].append(i)
            for i in range(i + 1, len(text)):
                if i == size - 1:
                    hashtag['indices'].append(size)
                elif text[i] == ' ':
                    hashtag['indices'].append(i)
                else:
                    continue
                hashtag['text'] = text[hashtag['indices'][0]:hashtag['indices'][1]]
                print(hashtag['text'])
                hashtag['id'] = 0
                hashtags.append(Hashtag(hashtag))
                break
        if text[i] == '@':
            mention['indices'].append(i)
            for i in range(i + 1, len(text)):
                if i == size - 1:
                    mention['indices'].append(size)
                elif text[i] == ' ':
                    mention['indices'].append(i)
                else:
                    continue
                mention['username'] = text[mention['indices'][0]+1:(mention['indices'][1])]
                mentions.append(Mention(mention))
                break
        i += 1
    return hashtags, mentions  # lists of objects
########################################################################################################################


def delete_kweek(kid):
    """
               Delete kweek with its credentials.


               *Parameters:*
                   - *kid*: The kweek id to be deleted   .

               *Returns:*
                   - *bool*: To indicate whether the deletion was successful or not.
                   - *message*: To specify the reason of failure if detected.

    """
    check, message = validate_request(kid)
    if not check:
        return check, message
    response = delete_main_kweek(kid)
    if response is not None:
        message = 'No such kweek to be deleted'
        return False, message
    response = update_hashtag()
    if response is not None:
        message = 'db failed'
        return False, message
    return True, None

########################################################################################################################


def validate_request(kid):
    """
                       Validate the request parametar.


                       *Parameters:*
                           - *kid*: The kweek id to be Validate.

                       *Returns:*
                           - *bool*: To indicate the validation result.
                           - *message*: To specify the reason of  mismatch if detected.

        """
    try:
        int(kid)
        check = validate_id(kid)
        if len(check) == 0:
            message = 'Kweek is not available '
            return False, message
        else:
            return True, None
    except ValueError:
        return False, 'invalid data type type '



def get_kweek(kid, authorized_username):
    """
                   Get the requested kweek with its credentials.


                   *Parameters:*
                       - *kid*: The id of the kweek to be retrieved   .

                   *Returns:*
                       - *bool*: To indicate whether the retrieval was successful or not.
                       - *message*: To specify the reason of failure if detected.
                       - *kweek object*: The kweek to be retrieved and its credentials.
                       - *list*: List of replies ids to the kweek

    """
    message = 'success'  # to be added
    check, message = validate_request(kid)
    if not check:
        return check, message, None, None
    hashtags = retrieve_hashtags(kid)  # rows of hahstag-kweek table (*)
    mentions = retrieve_mentions(kid)  # rows of mention table (*)
    replies = retrieve_replies(kid)  # rows of kweek table who is set as a reply yo the retrieved kweek (ids)
    rekweeks = retrieve_rekweeks(kid)  # rows of rekweeker table for those who rekweek the kweek (usernames)
    likers = retrieve_likers(kid)  # rows of likers table for those who liked the kweek (usernames)
    user = retrieve_user(kid)  # row of user profile table fo the user who wrote the kweek (*)
    hashtags_list = []  # list of hashtag objects
    mentions_list = []  # list of mention objects

    if hashtags:
        for hash in hashtags:
            Hid = hash['hashtag_id']
            s_index = hash['starting_index']
            e_index = hash['ending_index']
            indices = []
            indices.append(s_index)
            indices.append(e_index)
            text = retrieve_hashtag_text(Hid)
            hash_dic = {}
            hash_dic['id'] = Hid
            hash_dic['indices'] = indices
            hash_dic['text'] = text[0]['text']
            hashtag = Hashtag(hash_dic)
            hashtags_list.append(hashtag)

    if mentions:
        for ment in mentions:
            s_index = ment['starting_index']
            e_index = ment['ending_index']
            indices = []
            indices.append(s_index)
            indices.append(e_index)
            username = ment['username']
            ment_dic = {}
            ment_dic['indices'] = indices
            ment_dic['username'] = username
            mention = Mention(ment_dic)
            mentions_list.append(mention)

    if not user:
        return False, message, None, None  # a message may be added or something
    else:
        user = user[0]
        extrauser = {}
        me = authorized_username  # should be replaced by the function getting the current user
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

        check = check_blocked(me, user['username'])
        if check:
            extrauser['blocked'] = True
        else:
            extrauser['blocked'] = False
        check = check_muted(me, user['username'])
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

    rekweek_info = None
    kweekdic = {'hashtags': hashtags_list, 'mentions': mentions_list, 'number_of_likes': num_of_likes,
                'number_of_rekweeks': num_of_rekweeks, 'number_of_replies': num_of_replies,
                'rekweek_info': rekweek_info,
                'liked_by_user': liked_by_user, 'rekweeked_by_user': rekweeked_by_user, 'user': userobj}
    kweek = retrieve_kweek(kid)  # a row of kweek table
    kweek = kweek[0]
    kweekdic.update(kweek)
    kweekobj = Kweek(kweekdic)
    return True, message, kweekobj, replies


def get_kweek_with_replies(kid, username):
    """
                       Get the credentials of both requested kweek and its replies.


                       *Parameters:*
                           - *kid*: The id of the kweek to be retrieved   .

                       *Returns:*
                           - *bool*: To indicate whether the retrieval was successful or not.
                           - *message*: To specify the reason of failure if detected.
                           - *kweek object*: The kweek to be retrieved and its credentials.
                           - *list*: List of replies to the kweek being returned as kweek objects

    """

    replies_list_obj = []
    check, message, kweekobj, replies_list_dics = get_kweek(kid, username)
    if check:
        if replies_list_dics:
            for reply in replies_list_dics:
                id = reply['id']
                check2, message2, k, r = get_kweek(id,'hagar')
                if check2:
                    replies_list_obj.append(k)
                else:
                    message = 'db failed'
                    return check2, message2, None, None
    return check, message, kweekobj, replies_list_obj


