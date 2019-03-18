import database_manager
from models import Kweek, Hashtag,Mention
db_manager = database_manager.db_manager


def get_user(username):
    query = """ SELECT USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL FROM PROFILE WHERE USERNAME = %s"""
    data = (username, )
    response = db_manager.execute_query(query, data)
    print('0000000000000000000000000000000000000000000000000000000')
    print(response)
    return response


def add_kweek(kweek: Kweek):
    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s,%s,%s,%s,%s) """
    data = (kweek.created_at, kweek.text, kweek.media_url, kweek.user.username, kweek.reply_to)
    response = db_manager.execute_query_no_return(query, data)
    print('111111111111111111111111111111111111111111111111111111111111111')
    print(response)
    if response is not None:
        message = 'db failed'  #to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def get_kweek_id(kweek: Kweek):
    query: str = """SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """
    response = db_manager.execute_query(query)
    print('22222222222222222222222222222222222222222222222222')
    print(response)
    if type(response) == Exception:
        message = 'db failed'  # to be replaced
        return message, False, response
    elif len(response) == 0:
        message = 'db failed'  # to be replaced
        return message, False, response
    else:
        message = 'db succeeded'
        return message, True, response[0]['id']


def creat_mention(Kid, ment: Mention):
    query: str = """INSERT INTO MENTION VALUES(%s,%s,%s,%s) """
    data = (Kid, ment.username, ment.indices[0], ment.indices[1])
    response = db_manager.execute_query_no_return(query, data)
    print('333333333333333333333333333333333333333333333333')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def add_kweek_hashtag(Hid, Kid, hash: Hashtag):
    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (Kid, Hid, hash.indices[0], hash.indices[1],)
    response = db_manager.execute_query_no_return(query, data)
    print('444444444444444444444444444444444444444444444444444444444444444444444444444444444')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def create_hashtag(hash:Hashtag):
    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = (hash.text,)
    response = db_manager.execute_query_no_return(query, data)
    print('555555555555555555555555555555555555555555555555555555555555555555555555555')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def check_existing_hashtag(hashtag: Hashtag):
     query: str = """SELECT ID FROM HASHTAG WHERE TEXT =%s """
     data = (hashtag.text,)
     response = db_manager.execute_query(query, data)
     print('66666666666666666666666666666666666666666666666666')
     print(response)
     if type(response) == Exception:
         message = 'db failed'  # to be replaced
         return message, False, -1
     elif len(response) == 0:
         message = 'db failed'  # to be replaced
         return message, True, 0
     else:
         message = 'db succeeded'
         return message, True, response[0]['id']


########################################################################################################################
#################################################DELETE REKWEEK SECTION#################################################

def get_hashtags(id):
    query: str = """SELECT HASHTAG_ID FROM KWEEK_HASHTAG WHERE KWEEK_ID =%s """ #return list of dics
    data = (id,)
    response = db_manager.execute_query(query, data)
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(response)
    if type(response) == Exception:
        message = 'db failed'  # to be replaced
        return message, False, -1
    else:
        message = 'db succeeded'
        return message, True, response


def check_uniuqe_hash(id):
    query: str = """ SELECT COUNT(*) AS SUM  FROM KWEEK_HASHTAG WHERE HASHTAG_ID=%s ;"""  # return list of dics
    data = (id,)
    response = db_manager.execute_query(query, data)
    print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
    print(response)
    if type(response) == Exception:
        message = 'db failed'  # to be replaced
        return message, False, -1
    else:
        message = 'db succeeded'
        return message, True, response[0]['sum']


def delete_hashtag_H(id):
    query: str = """DELETE FROM HASHTAG WHERE ID=%s """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    print('cccccccccccccccccccccccccccccccccccccccccccccccccc')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def delete_hashtag_HK(id, kid):
    query: str = """DELETE FROM KWEEK_HASHTAG WHERE HASHTAG_ID=%s AND KWEEK_ID= %s"""
    data = (kid, id)
    response = db_manager.execute_query_no_return(query, data)
    print('dddddddddddddddddddddddddddddddddddddddddd')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def delete_rekweeks(id):
    query: str = """DELETE FROM REKWEEK WHERE KWEEK_ID=%s """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    print('ffffffffffffffffffffffffffffff')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def get_replies(id):
    print(id)
    query: str = """SELECT ID FROM KWEEK WHERE REPLY_TO =%s """  # return list of dics
    data = (id,)
    response = db_manager.execute_query(query, data)
    print('ggggggggggggggggggggggggggggggggggggggggggggggggg')
    print(response)
    if type(response) == Exception:
        message = 'db failed'  # to be replaced
        return message, False, response
    else:
        message = 'db succeeded'
        return message, True, response


def delete_likes(id):
    query: str = """DELETE FROM FAVORITE WHERE KWEEK_ID=%s """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True

def delete_mention(id):
    query: str = """DELETE FROM MENTION WHERE KWEEK_ID=%s """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True


def delete_main_kweek(id):
    query: str = """DELETE FROM KWEEK WHERE ID=%s """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    print(response)
    if response is not None:
        message = 'db failed'  # to be replaced
        return message, False
    else:
        message = 'db succeeded'
        return message, True

########################################################################################################################
#################################################GET REKWEEK SECTION#################################################

def retrieve_hashtags(kid:int):
    query: str = """SELECT * FROM KWEEK_HASHTAG WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check mentions retrieved ?/////////////////////////")
    print (response)
    return response


def retrieve_hashtag_text(Hid:int):
    query: str = """SELECT TEXT FROM HASHTAG WHERE  ID= %s"""
    data = (Hid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check hashtag text retrieved ?/////////////////////////")
    print (response)
    return response


def retrieve_mentions(kid:int):
    query: str = """SELECT * FROM MENTION WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check mentions retrieved ?/////////////////////////")
    print(response)
    return response

def retrieve_replies(kid:int):
    query: str = """SELECT ID FROM KWEEK WHERE  REPLY_TO= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check replies retrieved ?/////////////////////////")
    print(response)
    return response

def retrieve_rekweeks(kid:int):
    query: str = """SELECT * FROM REKWEEK WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check rekweeks retrieved ?/////////////////////////")
    print(response)
    return response

def retrieve_likers(kid:int):
    query: str = """SELECT USERNAME FROM FAVORITE WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check likers retrieved ?/////////////////////////")
    print(response)
    return response

def retrieve_user(kid:int):
    query: str = """SELECT * FROM PROFILE WHERE USERNAME IN (SELECT USERNAME FROM KWEEK WHERE ID=%s)"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check user retrieved ?/////////////////////////")
    print(response)
    return response


def check_following(me,user):
    query: str = """ SELECT * FROM FOLLOW WHERE FOLLOWED_USERNAME=%s AND FOLLOWER_USERNAME=%s ;"""
    data = (user,me)
    response = db_manager.execute_query(query, data)
    print("///////////////////check following ?/////////////////////////")
    print(response)
    return response

def check_muted(me,user):
    query: str = """ SELECT *  FROM MUTE WHERE MUTER_USERNAME=%s AND MUTED_USERNAME=%s;"""
    data = (user,me)
    response = db_manager.execute_query(query, data)
    print("///////////////////check muted ?/////////////////////////")
    print(response)
    return response

def check_blocked(me,user):
    query: str = """ SELECT * FROM BLOCK WHERE BLOCKER_USERNAME=%s AND BLOCKED_USERNAME=%s ;"""
    data = (user,me)
    response = db_manager.execute_query(query, data)
    print("///////////////////check blocked ?/////////////////////////")
    print(response)
    return response

def retrieve_kweek(kid:int):
    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    print("///////////////////check kweek retrieved ?/////////////////////////")
    print(response)
    return response








"""
    Create your functions here that contain only query construction logic.
    When passing parameters to queries use the method shown here:
    http://initd.org/psycopg/docs/usage.html

    Never use string concatenation or any other string formatting methods other than the one specified.

    You must check that the returned object is not an exception.

    The return of a SELECT query is a list of dictionaries, where each row is represented by a dictionary.
    The keys of the dictionary are the database column names.
"""
