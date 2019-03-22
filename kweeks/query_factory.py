import database_manager
from models import Kweek, Hashtag, Mention
db_manager = database_manager.db_manager


def get_user(username):
    query = """ SELECT USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL FROM PROFILE WHERE USERNAME = %s"""
    data = (username, )
    response = db_manager.execute_query(query, data)
    return response


def add_kweek(kweek: Kweek):
    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s,%s,%s,%s,%s) """
    data = (kweek.created_at, kweek.text, kweek.media_url, kweek.user.username, kweek.reply_to)
    db_manager.execute_query_no_return(query, data)


def get_kweek_id():
    query: str = """SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """
    response = db_manager.execute_query(query)
    return response


def create_mention(kid, ment: Mention):
    query: str = """INSERT INTO MENTION VALUES(%s,%s,%s,%s) """
    data = (kid, ment.username, ment.indices[0], ment.indices[1])
    response = db_manager.execute_query_no_return(query, data)
    return response


def add_kweek_hashtag(hid, kid, hash_obj: Hashtag):
    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid, hid, hash_obj.indices[0], hash_obj.indices[1],)
    db_manager.execute_query_no_return(query, data)



def create_hashtag(hash_obj: Hashtag):
    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = (hash_obj.text,)
    db_manager.execute_query_no_return(query, data)


def check_kweek_writer(kid, authorized_username):
    query: str = """SELECT * FROM KWEEK WHERE ID =%s AND USERNAME = %s  """
    data = (kid, authorized_username)
    response = db_manager.execute_query(query, data)
    return response


def check_existing_hashtag(hashtag: Hashtag):
    query: str = """SELECT ID FROM HASHTAG WHERE TEXT =%s """
    data = (hashtag.text,)
    response = db_manager.execute_query(query, data)
    return response


########################################################################################################################


def update_hashtag():
    query: str =\
        """ DELETE FROM HASHTAG WHERE ID NOT IN (SELECT HASHTAG_ID FROM KWEEK_HASHTAG WHERE HASHTAG_ID = ID); """
    data = (id,)
    response = db_manager.execute_query_no_return(query, data)
    return response


def delete_rekweeks(rid):
    query: str = """DELETE FROM REKWEEK WHERE KWEEK_ID=%s """
    data = (rid,)
    response = db_manager.execute_query_no_return(query, data)
    return response


def delete_likes(lid):
    query: str = """DELETE FROM FAVORITE WHERE KWEEK_ID=%s """
    data = (lid,)
    response = db_manager.execute_query_no_return(query, data)
    return response


def validate_id(kid):
    query: str = """SELECT * FROM KWEEK WHERE ID=%s """
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def delete_main_kweek(kid):
    query: str = """DELETE FROM KWEEK WHERE ID=%s """
    data = (kid,)
    response = db_manager.execute_query_no_return(query, data)
    return response


########################################################################################################################


def retrieve_hashtags(kid):
    query: str = """SELECT *, TEXT FROM KWEEK_HASHTAG JOIN HASHTAG  ON ID = HASHTAG_ID WHERE KWEEK_ID = %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_mentions(kid: int):
    query: str = """SELECT * FROM MENTION WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_replies(kid):
    query: str = """SELECT ID FROM KWEEK WHERE  REPLY_TO= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_rekweeks(kid):
    query: str = """SELECT * FROM REKWEEK WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_likers(kid):
    query: str = """SELECT USERNAME FROM FAVORITE WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_user(kid):
    query: str = """SELECT * FROM PROFILE WHERE USERNAME IN (SELECT USERNAME FROM KWEEK WHERE ID=%s)"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def check_following(me, user):
    query: str = """ SELECT * FROM FOLLOW WHERE FOLLOWED_USERNAME=%s AND FOLLOWER_USERNAME=%s ;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def check_muted(me, user):
    query: str = """ SELECT *  FROM MUTE WHERE MUTER_USERNAME=%s AND MUTED_USERNAME=%s;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def check_blocked(me, user):
    query: str = """ SELECT * FROM BLOCK WHERE BLOCKER_USERNAME=%s AND BLOCKED_USERNAME=%s ;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_kweek(kid):
    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response
