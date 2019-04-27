import database_manager

db_manager = database_manager.db_manager


def get_followers(username):
        """
                                    Query to get profile of followers users.

                                    *Parameters*:
                                        - *username (string)*: The username attribute in user_profile table .
                                    *Returns*:
                                        - *response*: The profile tuples of followers user .
        """
        query: str = """
                                    SELECT * FROM PROFILE WHERE USERNAME IN
                                    (SELECT FOLLOWER_USERNAME FROM FOLLOW WHERE FOLLOWED_USERNAME = %s)
                                    order by username;
                     """
        data = (username,)
        response = db_manager.execute_query(query, data)
        return response


def get_following(username):
        """
                                        Query to get profile of followed users.

                                        *Parameters*:
                                            - *username (string)*: The username attribute in user_profile table .
                                        *Returns*:
                                            - *response*: The profile tuples of followed user .
        """
        query: str = """
                                       SELECT * FROM PROFILE WHERE USERNAME IN
                                       (SELECT FOLLOWED_USERNAME FROM FOLLOW WHERE FOLLOWER_USERNAME = %s)
                                       order by username;
                     """
        data = (username,)
        response = db_manager.execute_query(query, data)
        return response


def check_if_follow(follower, followed):
        """
                                        Query to check if follow.

                                        *Parameters*:
                                            - *follower (string)*: The user that follow.
                                            - *followed (string)*: The user to be followed .
                                        *Returns*:
                                            - *response*: count if 0 then not following and if 1 then following.
        """
        query: str = """
                                    SELECT COUNT(*) FROM FOLLOW WHERE FOLLOWER_USERNAME = %s AND FOLLOWED_USERNAME = %s
                     """
        data = (follower, followed)
        response = db_manager.execute_query(query, data)[0]
        return response


def follow(authorized_username, username):
        """
                                         Query to add a user to the following list.

                                        *Parameters*:
                                            - *authorized_user (string)*: The user that follow.
                                            - *username (string)*: The user to be followed .
                                        *Returns*:
                                            - *response*: None if insert successfully.
        """
        query: str = """
                                    INSERT INTO FOLLOW (FOLLOWER_USERNAME, FOLLOWED_USERNAME) VALUES (%s, %s);
                     """
        data = (authorized_username, username)
        response = db_manager.execute_query_no_return(query, data)
        return response


def unfollow(authorized_username, username):
    """
                                    Query to remove a user from the following list.

                                    *Parameters*:
                                        - *authorized_user (string)*: The user that will unfollow.
                                        - *username (string)*: The user to be unfollowed .
                                    *Returns*:
                                        - *response*: None if delete successfully.
    """
    query: str = """
                                    DELETE FROM FOLLOW WHERE FOLLOWER_USERNAME = %s AND FOLLOWED_USERNAME = %s ;
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def get_muted_list(authorized_username):
    """
                                    Query to get muted list for muter user.

                                    *Parameters*:
                                        - *authorized_user (string)*: The muter user.
                                    *Returns*:
                                        - *response*: list of muted user.
    """
    query: str = """
                                    SELECT USERNAME,SCREEN_NAME,PROFILE_IMAGE_URL FROM PROFILE WHERE USERNAME IN
                                    (SELECT MUTED_USERNAME FROM MUTE  WHERE MUTER_USERNAME = %s)
                                    order by username;
                 """
    data = (authorized_username,)
    response = db_manager.execute_query(query, data)
    return response


def if_muted(authorized_username, username):
    """
                                    Query to check if user is muted before.

                                    *Parameters*:
                                        - *authorized_username(string)*: The muter user.
                                        - *username (string)*: The muted user .
                                    *Returns*:
                                        - *response*: count if 0 then not muted and if 1 then muted.
    """
    query: str = """
                                SELECT COUNT(*) FROM MUTE WHERE MUTER_USERNAME = %s AND MUTED_USERNAME = %s
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query(query, data)[0]
    return response


def mute(authorized_username, username):
    """
                                    Query to add a muted user to the muting list.

                                    *Parameters*:
                                        - *authorized_user (string)*:The muter user.
                                        - *username (string)*:The muted user .
                                    *Returns*:
                                        - *response*: None if insert successfully.
    """
    query: str = """
                                INSERT INTO MUTE (MUTER_USERNAME, MUTED_USERNAME) VALUES (%s, %s);
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def unmute(authorized_username, username):
    """
                                    Query to remove a muted user from the muting list.

                                    *Parameters*:
                                        - *authorized_user (string)*: The muter user.
                                        - *username (string)*:The muted user .
                                    *Returns*:
                                        - *response*: None if delete successfully.
    """
    query: str = """
                                    DELETE FROM MUTE WHERE MUTER_username = %s AND MUTED_username = %s ;
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def get_blocked_list(authorized_username):
    """
                                    Query to get blocked list for muter user.

                                    *Parameters*:
                                        - *authorized_user (string)*: The blocker user.
                                    *Returns*:
                                        - *response*: list of blocked user.
    """
    query: str = """
                                    SELECT USERNAME,SCREEN_NAME,PROFILE_IMAGE_URL FROM PROFILE WHERE USERNAME IN
                                    (SELECT BLOCKED_USERNAME FROM BLOCK  WHERE BLOCKER_USERNAME = %s)
                                    order by username;
                 """
    data = (authorized_username,)
    response = db_manager.execute_query(query, data)
    return response


def if_blocked(authorized_username, username):
    """
                                    Query to check if user is blocked before.

                                    *Parameters*:
                                        - *authorized_username(string)*: The blocker user.
                                        - *username (string)*: The blocked user .
                                    *Returns*:
                                        - *response*: count if 0 then not blocked and if 1 then blocked.
    """
    query: str = """
                                SELECT COUNT(*) FROM BLOCK WHERE BLOCKER_USERNAME = %s AND BLOCKED_USERNAME = %s
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query(query, data)[0]
    return response


def block(authorized_username, username):
    """
                                    Query to add a blocked user into the blocking list.

                                    *Parameters*:
                                        - *authorized_user (string)*:The blocker user.
                                        - *username (string)*:The blocked user .
                                    *Returns*:
                                        - *response*: None if insert successfully.
    """
    query: str = """
                                INSERT INTO BLOCK (BLOCKER_USERNAME, BLOCKED_USERNAME) VALUES (%s, %s);
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def unblock(authorized_username, username):
    """
                                    Query to remove a blocked user from the blocking list.

                                    *Parameters*:
                                        - *authorized_user (string)*:The blocker user.
                                        - *username (string)*:The blocked user .
                                    *Returns*:
                                        - *response*: None if delete successfully.
    """
    query: str = """
                                DELETE FROM BLOCK WHERE BLOCKER_USERNAME = %s AND BLOCKED_USERNAME = %s ;
                 """
    data = (authorized_username, username)
    response = db_manager.execute_query_no_return(query, data)
    return response
