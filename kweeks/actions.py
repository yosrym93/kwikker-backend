
from datetime import datetime
from models import Kweek, Hashtag, Mention, User, RekweekInfo
from kweeks.query_factory import add_kweek, get_hashtags, check_uniuqe_hash, delete_hashtag_H, delete_hashtag_HK\
    , delete_rekweeks, get_replies, delete_likes, delete_mention, delete_main_kweek, retrieve_hashtags\
    , retrieve_mentions, retrieve_replies, retrieve_rekweeks, retrieve_user, retrieve_likers, retrieve_hashtag_text\
    , check_following, check_blocked, check_muted, retrieve_kweek, get_user, add_kweek_hashtag, creat_mention\
    , create_hashtag, check_existing_hashtag, get_kweek_id


"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def create_kweek(request, logged_in_user):
    data = {}
    text = request['text']
    hashtags, mentions = extract_mentions_hashtags(text)  # two lists of objects
    userr = get_user(logged_in_user)
    if type(userr)is Exception:
        message = 'error retrieving the user'
        return False, message
    else:
        if len(userr) == 0:
            message = 'no such user'
            return False, message
        else:
            userr=userr[0]
    dic = {'following': None, 'follows_you': None, 'blocked': None, 'muted': None}
    userr.update(dic)
    user = User(userr)  #user obj
    data['id'] = 0
    data['created_at'] = datetime.utcnow()
    data['username'] = logged_in_user  #to be changed
    data['hashtags'] = hashtags  #list of dics
    data['mentions'] = mentions  #list of dics
    data['media_url'] = None
    data['number_of_likes'] = 0
    data['number_of_rekweeks'] = 0
    data['number_of_replies'] = 0
    data['rekweek_info'] = None
    data['liked_by_user'] = False
    data['rekweeked_by_user'] = False
    data['user'] = user
    data.update(request)
    kweek = Kweek(data)  #kweek obj
    print(kweek)
    message = insert_kweek(kweek)
    print(message)
    return message


def insert_kweek(kweek: Kweek):
    message, check = add_kweek(kweek)
    if not check:
        return message
    message, check, kid = get_kweek_id(kweek)
    if not check:
        return message
    for hash in kweek.hashtags:  #if no hahstags available it won't enter the loop
        message, check, test = check_existing_hashtag(hash)
        if not check:
                return message
        elif test == 0:  # then it is a new hashtag
            message, check = create_hashtag(hash)  #create a new hashtag
            if not check:
                return message
            message, check, id = check_existing_hashtag(hash)  #then insert it into kweek-hashtag table
            if not check:
                return message
            elif id == 0:
                return message
            else:
                hid = id
        else:
            hid = test
        message, check = add_kweek_hashtag(hid, kid, hash)
        if not check:
            return message

    for ment in kweek.mentions:
        message, check = creat_mention(kid, ment)
        if not check:
            return message
    message ='every thing went fine'  #then to be replaced
    return message


def extract_mentions_hashtags(text):
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
    return hashtags, mentions  #lists of objects
########################################################################################################################
#################################################DELETE REKWEEK SECTION#################################################

    # 1- get hahstags ids of the rows with kid= id in k-h table, list of dics each dic contains id
    # 2- loop on that list, for each hashtag, check if exists in h-k table with id other than id
    # 3- if yes, delete it form h-k only, if no, delete it from h table also
    # 4- delete any mention in mentions table with kid =id
    # 5- delete any rekweek with kid=id
    # 6- delete any kweek with reply_to = id
    # 7-delete any like to that rekweek


def delete_kweek(kid: int):
    message, check, hashtags = get_hashtags(kid)  #list of dics of kweek hashtags (ids)
    if not check:
        return message
    if hashtags is not None:
        for hash in hashtags:  # if no hahstags available it won't enter the loop
            message, check, response = check_uniuqe_hash(hash['hashtag_id'])
            if not check:
                return message
            elif response == 1:  # then it is a unique hashtag
                message, check = delete_hashtag_HK(kid, hash['hashtag_id'])
                if not check:
                    return message
                message, check = delete_hashtag_H(hash['hashtag_id'])
                if not check:
                    return message
            else:
                message, check = delete_hashtag_HK(kid, hash['hashtag_id'])
            if not check:
                return message

    message, check = delete_rekweeks(kid)
    if not check:
        return message

    message, check = delete_mention(kid)
    if not check:
        return message

    message, check = delete_likes(kid)
    if not check:
        return message

    message, check, response = get_replies(kid)  #list of dics of replies ids
    if not check:
        return message
    else:
        if response is not None :
            print('enteredd')
            print(response)
            for reply in response:
                print(reply)
                message, check = delete_kweek(reply['id'])
                if not check:
                    return message


    message, check = delete_main_kweek(kid)
    if not check:
        return message
    message = 'every thing went fine'  # then to be replaced
    return message

########################################################################################################################
#################################################GET REKWEEK SECTION####################################################


def get_kweek(kid):
    message, check , hashtags = retrieve_hashtags(kid) #rows of hahstag-kweek table (*)
    if type(hashtags) == Exception:
        return False
    mentions = retrieve_mentions(kid)#rows of mention table (*)
    if type(mentions) == Exception:
        return False
    replies = retrieve_replies(kid)#rows of kweek table who is set as a reply yo the retrieved kweek (ids)
    if type(replies) == Exception:
        return False
    rekweeks = retrieve_rekweeks(kid) #rows of rekweeker table for those who rekweek the kweek (usernames)
    if type(rekweeks) == Exception:
        return False
    likers = retrieve_likers(kid) #rows of likers table for those who liked the kweek (usernames)
    if type(likers) == Exception:
        return False
    user = retrieve_user(kid) # row of user profile table fo the user who wrote the kweek (*)
    if type(user) == Exception:
        return False
    hashtags_list = [] #list of hashtag objects
    mentions_list = []  # list of mention objects
    if hashtags is not None:
        for hash in hashtags:
            Hid = hash['hashtag_id']
            s_index = hash['starting_index']
            e_index = hash['ending_index']
            indices = []
            indices.append(s_index)
            indices.append(e_index)
            text = retrieve_hashtag_text(Hid)
            if type(text) == Exception:
                return False
            else:
                hash_dic = {}
                hash_dic['id'] = Hid
                hash_dic['indices'] = indices
                print(text,'/////////////////////////text//////////////////////////')
                hash_dic['text'] = text[0]['text']
            hashtag = Hashtag(hash_dic)
            hashtags_list.append(hashtag)
            print("///////////////////hashtags_list ?/////////////////////////")
            print(hashtags_list)

    if mentions is not None:
        for ment in mentions:
            s_index = ment['starting_index']
            e_index = ment['ending_inex']
            indices = []
            indices.append(s_index)
            indices.append(e_index)
            username = ment['username'][0]['text']
            ment_dic = {}
            ment_dic['indices'] = indices
            ment_dic['username'] = username
            mention = Mention(ment_dic)
            mentions_list.append(mention)
            print("///////////////////mentions_list ?/////////////////////////")
            print(mentions_list)

    if user is None:
        return False  # a message may be added or something
    else:
        user = user[0]
        extrauser = {}
        me = 'default'  # should be replaced by the function getting the current user
        check = check_following(me, user['username'])
        print('//////////////////check following//////////////////')
        print(check)
        if type(check) == Exception:
            return False
        else:
            if check is not None:
                extrauser['following'] = True
            else:
                extrauser['following'] = False

        check = check_following(user['username'], me)
        if type(check) == Exception:
            return False
        else:
            if check is not None:
                extrauser['follows_you'] = True
            else:
                extrauser['follows_you'] = False

        check = check_blocked(me, user['username'])
        if type(check) == Exception:
            return False
        else:
            if check is not None:
                extrauser['blocked'] = True
            else:
                extrauser['blocked'] = False

        check = check_muted(me, user['username'])
        if type(check) == Exception:
            return False
        else:
            if check:
                extrauser['muted'] = True
            else:
                extrauser['muted'] = False
        extrauser.update(user)

    userobj = User(extrauser)
    print("///////////////////userobj ?/////////////////////////")
    print(userobj)

    if replies is not None:
        num_of_replies = len(replies)
    else:
        num_of_replies = 0

    if likers is not None:
        num_of_likes = len(likers)
        liked_by_user = {'username': me} in likers
    else:
        num_of_likes = 0
        liked_by_user = False

    if mentions is not None:
        num_of_mentions = len(mentions)
    else:
        num_of_mentions = 0

    if rekweeks is not None:
        num_of_rekweeks = len(rekweeks)
        rekweeked_by_user = {'username': me} in rekweeks
    else:
        num_of_mentions = 0
        rekweeked_by_user = False

    rec_info_dic = {'rekweeker_name': 'smth', 'rekweeker_username': 'smth '}
    rekweek_info = RekweekInfo(rec_info_dic)
    print(rekweek_info)
    kweekdic = {'hashtags': hashtags_list, 'mentions': mentions_list, 'number_of_likes': num_of_likes,
                'number_of_rekweeks': num_of_rekweeks, 'number_of_replies': num_of_replies,
                'rekweek_info': rekweek_info,
                'liked_by_user': liked_by_user, 'rekweeked_by_user': rekweeked_by_user, 'user': userobj}
    print(kweekdic)
    kweek = retrieve_kweek(kid)  # a row of kweek table
    if type(kweek) == Exception:
        return False
    else:
        if kweek is not None:
            kweek = kweek[0]
            kweekdic.update(kweek)
        else:
            return False
        print("///////////////////kweek dic ?/////////////////////////")
        print(kweekdic)
    kweekobj = Kweek(kweekdic)
    print("/////////////////// kweek obj ?/////////////////////////")
    print(kweekobj)
    print(replies)
    return kweekobj, replies


def get_kweek_with_replies(kid: int):
    replies_list_obj = []
    kweekobj, replies_list_dics = get_kweek(kid)
    if replies_list_dics is not None:
        for reply in replies_list_dics:
            id = reply['id']
            k, r = get_kweek(id)
            replies_list_obj.append(k)
        print("///////////////////replies_list ?/////////////////////////")
        print(replies_list_obj)
        print("///////////////////kweek ?/////////////////////////")
        print(kweekobj)
    return kweekobj, replies_list_obj



























