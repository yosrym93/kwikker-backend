import database_manager

db_manager = database_manager.db_manager


# Returns kweeks with the basic data: id, created_at, text, media_url, username, reply_to
def get_profile_kweeks(username):
    query = """
                SELECT ID, CREATED_AT, TEXT, MEDIA_URL, USERNAME, REPLY_TO, IS_REKWEEK FROM
                (
                (SELECT TRUE as IS_REKWEEK, K.ID, K.CREATED_AT, K.TEXT, K.MEDIA_URL, K.USERNAME, K.REPLY_TO, 
                        RK.CREATED_AT AS SORT_BY 
                 FROM KWEEK K
                 JOIN REKWEEK RK ON RK.KWEEK_ID = K.ID
                 WHERE RK.USERNAME = %s)

                UNION

                (SELECT FALSE as IS_REKWEEK, *, CREATED_AT AS SORT_BY FROM KWEEK WHERE USERNAME = %s)
                ) AS KWEEKS
                ORDER BY SORT_BY 
            """

    data = (username, username)
    profile_kweeks = db_manager.execute_query(query, data)
    return profile_kweeks


# Returns statistics of a kweek: number_of_likes, rekweeks, replies, is_liked_by_user, is_rekweeked_by_user
def get_kweek_statistics(kweek_id, authorized_username):
    kweek_statistics = {}

    # Number of likes
    query = """
                SELECT COUNT(*) FROM FAVORITE WHERE KWEEK_ID = %s
            """
    data = (kweek_id, )
    kweek_statistics['number_of_likes'] = db_manager.execute_query(query, data)[0].get('count')

    # Number of rekweeks
    query = """
                SELECT COUNT(*) FROM REKWEEK WHERE KWEEK_ID = %s
            """
    kweek_statistics['number_of_rekweeks'] = db_manager.execute_query(query, data)[0].get('count')

    # Number of replies
    query = """
                SELECT COUNT(*) FROM KWEEK WHERE REPLY_TO = %s 
            """
    kweek_statistics['number_of_replies'] = db_manager.execute_query(query, data)[0].get('count')

    # Is liked by the authorized user
    query = """
                SELECT * FROM FAVORITE
                WHERE KWEEK_ID = %s AND USERNAME = %s
            """
    data = (kweek_id, authorized_username)
    if not db_manager.execute_query(query, data):
        kweek_statistics['liked_by_user'] = False
    else:
        kweek_statistics['liked_by_user'] = True

    # Is rekweeked by the authorized user
    query = """
                SELECT * FROM REKWEEK
                WHERE KWEEK_ID = %s AND USERNAME = %s
            """
    data = (kweek_id, authorized_username)
    if not db_manager.execute_query(query, data):
        kweek_statistics['rekweeked_by_user'] = False
    else:
        kweek_statistics['rekweeked_by_user'] = True

    return kweek_statistics


def get_kweek_mentions(kweek_id):
    query = """
                SELECT * FROM MENTION WHERE KWEEK_ID = %s
            """
    data = (kweek_id,)
    mentions = db_manager.execute_query(query, data)
    return mentions


def get_kweek_hashtags(kweek_id):
    query = """
                SELECT * FROM KWEEK_HASHTAG WHERE KWEEK_ID = %s
            """
    data = (kweek_id,)
    hashtags = db_manager.execute_query(query, data)
    return hashtags


def get_user_data(required_username):
    query = """
                SELECT USERNAME, SCREEN_NAME, PROFILE_IMAGE_URL FROM PROFILE
                WHERE USERNAME = %s
            """
    data = (required_username, )
    user = db_manager.execute_query(query, data)[0]
    return user


def get_friendship(authorized_username, required_username):
    # The friendship checks are invalid if the authorized username is the same as the required username
    friendship = {}
    if authorized_username == required_username:
        friendship['following'] = None
        friendship['follows_you'] = None
        friendship['blocked'] = None
        friendship['muted'] = None
        return friendship

    # Following
    query = """
                SELECT * FROM FOLLOW WHERE FOLLOWER_USERNAME = %s AND FOLLOWED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        friendship['following'] = False
    else:
        friendship['following'] = True

    # Follows you
    data = (required_username, authorized_username)
    if not db_manager.execute_query(query, data):
        friendship['follows_you'] = False
    else:
        friendship['follows_you'] = True

    # Muted
    query = """
                SELECT * FROM MUTE WHERE MUTER_USERNAME = %s AND MUTED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        friendship['muted'] = False
    else:
        friendship['muted'] = True

    # Muted
    query = """
                SELECT * FROM BLOCK WHERE BLOCKER_USERNAME = %s AND BLOCKED_USERNAME = %s
            """
    data = (authorized_username, required_username)
    if not db_manager.execute_query(query, data):
        friendship['blocked'] = False
    else:
        friendship['blocked'] = True

    return friendship


def is_user(username):
    query = """
                SELECT * FROM USER_CREDENTIALS WHERE USERNAME = %s
            """
    data = (username,)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True
