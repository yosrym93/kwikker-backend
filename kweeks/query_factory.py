import database_manager
from models import Kweek, Hashtag, Mention
from datetime import datetime
db_manager = database_manager.db_manager


def get_user(username):
    """
                   Query to get user profile from the database.

                   *Parameters*:
                       - *username (string)*: The username attribute in user_profile table.

                   *Returns*:
                       - *response*: A dictionary contains user profile tuples  .
       """
    query = """ SELECT USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL FROM PROFILE WHERE USERNAME = %s"""
    data = (username, )
    response = db_manager.execute_query(query, data)
    return response


def add_kweek(kweek: Kweek):
    """
                   Query to insert kweek into the data base.

                   *Parameters*:
                       - *kweek (object)*: The kweek object to be inserted.

       """
    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s,%s,%s,%s,%s) """
    data = (kweek.created_at, kweek.text, kweek.media_url, kweek.user.username, kweek.reply_to)
    db_manager.execute_query_no_return(query, data)


def get_kweek_id():
    """
                   Query to get the last kweek id inserted in the data base.


                   *Returns*:
                       - *response*: A list of dictionary containing the  kweek id   .
       """
    query: str = """SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """
    response = db_manager.execute_query(query)
    return response


def create_mention(kid, ment: Mention):
    """
                   Query to insert a mention in the database.

                   *Parameters*:
                        -*ment(object)*: The mention object to get inserted.
                        - *id*: The id of the kweek including the mention .

       """
    query: str = """INSERT INTO MENTION VALUES(%s,%s,%s,%s) """
    data = (kid, ment.username, ment.indices[0], ment.indices[1])
    response = db_manager.execute_query_no_return(query, data)
    return response


def add_kweek_hashtag(hid, kid, hash_obj: Hashtag):
    """
                  Query to insert hashtag in the kweek_hashtag table.

                  *Parameters*:
                      - *hid*: The id of the hashtag to get inserted.
                      - *kid*: The id of the mention to get inserted.
                      - *hash_obj(object)*: The hashtag object to get inserted.

    """

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid, hid, hash_obj.indices[0], hash_obj.indices[1],)
    db_manager.execute_query_no_return(query, data)


def create_hashtag(hash_obj: Hashtag):
    """
                  Query to insert hashtag in the hashtag table.

                  *Parameters*:
                      - *hash_obj(object)*: The hashtag object to get inserted.

    """

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = (hash_obj.text,)
    db_manager.execute_query_no_return(query, data)


def check_kweek_writer(kid, authorized_username):
    """
                  Query to get the user if it was the writer of a particular kweek .

                  *Parameters*:
                      - *kid*: The id of the kweek to be checked.
                      - *authorized_username(string)*: The user currently logged in.

                  *Returns*:
                      - *response*: A list of dictionary containing the user tuple   .

        """

    query: str = """SELECT * FROM KWEEK WHERE USERNAME =%s AND ID= %s  """
    data = (authorized_username, kid)
    response = db_manager.execute_query(query, data)
    return response


def check_kweek_owner(kid, authorized_username):
    """
                  Query to get the logged in user if it was the writer of a kweek that got replied to by
                  a particular kweek.

                  *Parameters*:
                      - *kid*: The id of the reply  to be checked.
                      - *authorized_username(string)*: The user currently logged in.

                  *Returns*:
                      - *response*: A list of dictionary as the user tuple.

    """

    query: str = """SELECT * FROM KWEEK REPLY JOIN KWEEK POST ON REPLY.REPLY_TO = POST.ID 
     WHERE POST.USERNAME =%s AND REPLY.ID= %s  """
    data = (authorized_username, kid)
    response = db_manager.execute_query(query, data)
    return response


def check_existing_hashtag(hashtag: Hashtag):
    """
                    Query to check if that hashtag exist already in the data base.

                    *Parameters*:
                        - *hashtag(object)*: The hashtag object to be checked.

                    *Returns*:
                        -*response*: The id of the hashtag if found .
    """

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT =%s """
    data = (hashtag.text,)
    response = db_manager.execute_query(query, data)
    return response


def check_kweek_mention(kid, ment: Mention):
    """
                   Query to check if a mention exist already for th same kweek id.

                   *Parameters*:
                       - *ment(object)*: The mention object to be checked.
                       - *kid*: The id of the kweek to be checked.


                   *Returns*:
                       -*response*: The count to indicate found or not.
    """

    query: str = """SELECT COUNT(*) FROM MENTION WHERE KWEEK_ID =%s AND USERNAME =%s """
    data = (kid, ment.username)
    response = db_manager.execute_query(query, data)
    return response


########################################################################################################################


def update_hashtag():
    """
                   Query to delete the hashtag form the hashtag table if it was the last one in the kweek_hashtag table.

    """

    query: str =\
        """ DELETE FROM HASHTAG WHERE ID NOT IN (SELECT HASHTAG_ID FROM KWEEK_HASHTAG WHERE HASHTAG_ID = ID); """
    db_manager.execute_query_no_return(query)


def delete_rekweeks(rid):
    """
                   Query to delete the rekweeks of a particular kweek.

                   *Parameters*:
                       - *rid*: The id of the kweek to be rekweeked.

    """

    query: str = """DELETE FROM REKWEEK WHERE KWEEK_ID=%s """
    data = (rid,)
    db_manager.execute_query_no_return(query, data)


def delete_like(lid, authorized_username):
    """
                   Query to delete the likes for a particular kweek.

                   *Parameters*:
                       - *lid*: The id of the kweek to be liked.
                       - *authorized_username(string)*: The user currently logged in.

    """
    query: str = """DELETE FROM FAVORITE WHERE KWEEK_ID=%s AND USERNAME=%s"""
    data = (lid, authorized_username)
    db_manager.execute_query_no_return(query, data)


def validate_id(kid):
    """
                   Query to check if a kweek id is valid or not .

                   *Parameters*:
                       - *kid*: The id of the kweek to be checked.

                   *Returns*:
                       -*response*: A tuple the kweek to indicate whether valid or not.

   """
    query: str = """SELECT * FROM KWEEK WHERE ID=%s """
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def delete_main_kweek(kid):
    """
                   Query to delete a particular kweek.

                   *Parameters*:
                       - *kid*: The id of the kweek to be deleted.

    """
    query: str = """DELETE FROM KWEEK WHERE ID=%s """
    data = (kid,)
    db_manager.execute_query_no_return(query, data)

########################################################################################################################


def retrieve_hashtags(kid):
    """
                   Gets the hashtags in a given kweek.


                   *Parameters:*
                       - *kid*: The id of the kweek.

                   *Returns:*
                       - *List of dictionaries*: {
                                           | *hashtag_id (int)*: The id of the hashtag.,
                                           | *starting_index (int)*: The starting index of the hashtag in the kweek.,
                                           | *ending_index (int)*: The ending index of the hashtag in the kweek.,
                                           | *kweek_id (int)*: The id of the kweek.
                                           | }
    """
    query: str = """SELECT *, TEXT FROM KWEEK_HASHTAG JOIN HASHTAG  ON ID = HASHTAG_ID WHERE KWEEK_ID = %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_mentions(kid: int):
    """
                   Gets the mentions in a given kweek.


                   *Parameters:*
                       - *kweek_id*: The id of the kweek.

                   *Returns:*
                       - *List of dictionaries*: {
                                           | *username (string)*: The username of the mentioned user.,
                                           | *starting_index (int)*: The starting index of the mention in the kweek.,
                                           | *ending_index (int)*: The ending index of the mention in the kweek.,
                                           | *kweek_id (int)*: The id of the kweek.
                                           | }
    """
    query: str = """SELECT * FROM MENTION WHERE  KWEEK_ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_replies(kid):
    """
                   Gets the replies on a given kweek.


                   *Parameters:*
                       - *kid*: The id of the kweek.

                   *Returns:*
                       - *response*: A list of dictionaries of replies id.

    """
    query: str = """SELECT ID FROM KWEEK WHERE  REPLY_TO= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_user(kweek_id, num):
    """
                   Gets the profile of the writer for a given kweek .


                   *Parameters:*
                       - *kid*: The id of the kweek.
                       - *number*: the number of the query to be executed, .

                   *Returns:*
                       - *response*: A list of dictionary of the user tuple .

    """
    response = None
    query1: str = """SELECT * FROM PROFILE WHERE USERNAME IN (SELECT USERNAME FROM KWEEK WHERE ID=%s)"""
    query2: str = """SELECT * FROM PROFILE WHERE USERNAME = (SELECT USERNAME FROM FAVORITE WHERE  KWEEK_ID= %s)"""
    query3: str = """SELECT * FROM PROFILE WHERE USERNAME = (SELECT USERNAME FROM REKWEEK WHERE  KWEEK_ID= %s)"""
    data = (kweek_id,)
    if num == 1:
        response = db_manager.execute_query(query1, data)
    elif num == 2:
        response = db_manager.execute_query(query2, data)
    elif num == 3:
        response = db_manager.execute_query(query3, data)
    return response


def check_following(me, user):
    """
                    Checks if the a user is followed by another user.


                    *Parameters:*
                        - *me*: The username of the first user.
                        - *user*: The username of the second user.

                    *Returns:*
                        - The tuple having the matched results.
    """
    query: str = """ SELECT * FROM FOLLOW WHERE FOLLOWED_USERNAME=%s AND FOLLOWER_USERNAME=%s ;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def check_muted(me, user):
    """
                    Checks if the authorized user is muting the required user.


                    *Parameters:*
                        - *me*: The username of the authorized user.
                        - *user*: The username of the required user.

                    *Returns:*
                        - The tuple having the matched results.

    """
    query: str = """ SELECT *  FROM MUTE WHERE MUTER_USERNAME=%s AND MUTED_USERNAME=%s;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def check_blocked(me, user):
    """
                   Checks if the authorized user is blocking the required user.


                   *Parameters:*
                       - *me*: The username of the authorized user.
                       - *user*: The username of the required user.

                   *Returns:*
                       - The tuple having the matched results.

    """

    query: str = """ SELECT * FROM BLOCK WHERE BLOCKER_USERNAME=%s AND BLOCKED_USERNAME=%s ;"""
    data = (user, me)
    response = db_manager.execute_query(query, data)
    return response


def retrieve_kweek(kid):
    """
                   Gets the kweek of a given id.


                   *Parameters:*
                       - *kid*: The id of the kweek.

                   *Returns:*
                       - *response*: A list of dictionary as the kweek tuple.

    """
    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid,)
    response = db_manager.execute_query(query, data)
    return response


def add_rekweek(kweek_id, authorized_username):
    """
                   Query to insert rekweek into the data base.

                   *Parameters*:
                       - *kweek_id (string)*: The kweek id to be rekweeked.
                       - *authorized_username(string)*: The user currently logged in.

    """
    query: str = """INSERT INTO  REKWEEK (USERNAME,KWEEK_ID,CREATED_AT) VALUES(%s,%s,%s) """
    data = (authorized_username, kweek_id, datetime.utcnow())
    db_manager.execute_query_no_return(query, data)


def check_kweek_rekweeker(kid, authorized_username):
    """
                  Query to get the user if it was the writer of a particular kweek .

                  *Parameters*:
                      - *kid*: The id of the kweek to be checked.
                      - *authorized_username(string)*: The user currently logged in.

                  *Returns*:
                      - *response*: A list of dictionary containing the rekweek tuple   .

        """

    query: str = """SELECT * FROM REKWEEK WHERE USERNAME =%s AND KWEEK_ID= %s  """
    data = (authorized_username, kid)
    response = db_manager.execute_query(query, data)
    return response


def add_like(kweek_id, authorized_username):
    """
                      Query to update likes of a kweek .

                      *Parameters*:
                          - *kweek_id (string)*: The kweek id to be rekweeked.
                          - *authorized_username(string)*: The user currently logged in.


       """
    query: str = """INSERT INTO  FAVORITE (USERNAME,KWEEK_ID,CREATED_AT) VALUES(%s,%s,%s) """
    data = (authorized_username, kweek_id, datetime.utcnow())
    db_manager.execute_query_no_return(query, data)
