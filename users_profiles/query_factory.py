import database_manager

db_manager = database_manager.db_manager


def get_user_profile(username):
    """
                                Query to get user profile from database.

                                *Parameters*:
                                    - *username (string)*: The username attribute in user_profile table.

                                *Returns*:
                                    - *response*: a dictionary contains user profile tuples  .
    """
    query: str = """
                     select * from profile where username=%s 

                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def update_user_profile(username, bio, screen_name):
    """
                                Query to updates bio and screen name in user profile.

                                *Parameters*:
                                    - *username (string)*: The username attribute in user_profile table.
                                    - *bio (text)*: The updated biography of the user.
                                    - *screen_name(string)*: The updated name shown on profile screen.
                                *Returns*:
                                    -*response*: which is none of case in successful update .
    """
    if bio == '' or bio is None:
        query: str = """
                                update profile set screen_name = %s where username = %s
                         """
        data = (screen_name, username)
        response = db_manager.execute_query_no_return(query, data)
        return response

    elif screen_name == '' or screen_name is None:
        query: str = """
                                update profile set bio = %s  where username = %s
                         """
        data = (bio, username)
        response = db_manager.execute_query_no_return(query, data)
        return response

    else:
        query: str = """
                                update profile set bio = %s , screen_name = %s where username = %s
                         """
        data = (bio, screen_name, username)
        response = db_manager.execute_query_no_return(query, data)
        return response


def update_user_profile_picture(username, filename):
    """
                                Query updates profile picture.

                                *Parameters*:
                                    - *username (string)*: The username attribute in user_profile table .
                                    - *filename (file)*: The profile image name which will be updated in database.
                                *Returns*:
                                    - *response*: which is none of case in successful update .
    """
    query: str = """
                        update profile set profile_image_url = %s where username = %s
                 """
    data = (filename, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def update_user_banner_picture(username, filename):
    """
                                Query updates profile banner.

                                *Parameters*:
                                    - *username (string)*: The username attribute in user_profile table .
                                    - *filename (file)*: The profile banner name which will be updated in database.
                                *Returns*:
                                    - *response*: which is none of case in successful update .
    """
    query: str = """
                      update profile set profile_banner_url = %s where username = %s
                 """
    data = (filename, username)
    response = db_manager.execute_query_no_return(query, data)
    return response


def get_user_followers(username):
    """
                                Query to get number of followers.

                                *Parameters*:
                                    - *username (string)*: The username attribute in user_profile table .
                                *Returns*:
                                    - *response*: The number of followers .
    """
    query: str = """
                         select count(*) from follow where followed_username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def get_user_following(username):
    """
                                    Query to get number of following.

                                    *Parameters*:
                                        - *username (string)*: The username attribute in user_profile table .
                                    Returns:
                                        - *response*: The number of following .
    """
    query: str = """
                         select count(*) from follow where follower_username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def get_number_of_kweeks(username):
    """
                                    Query to get number of kweeks posted by the user.

                                    *Parameters*:
                                        - *username (string)*: The username attribute in user_profile table .
                                    *Returns*:
                                        - *response*: The number of kweeks .
    """
    query: str = """
                         select count(*) from kweek where username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def get_number_of_likes(username):
    """
                                    Query to get number of likes the user made.

                                    *Parameters*:
                                        - *username (string)*: The username attribute in user_profile table .
                                    *Returns*:
                                        - *response*: The number of likes.
    """
    query: str = """
                        select count(*) from favorite where username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def get_user_profile_picture(username):
    """
                                        Query to get name of  profile picture.

                                        *Parameters*:
                                            - *username (string)*: The username attribute in user_profile table .
                                        *Returns*:
                                            - *response*: The name of  profile picture.
    """
    query: str = """
                            select profile_image_url from profile where username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def get_user_banner_picture(username):
    """
                                            Query to get name of banner picture.

                                            *Parameters*:
                                                - *username (string)*: The username attribute in user_profile table .
                                            *Returns*:
                                                - *response*: The name of banner picture.
    """
    query: str = """
                                select profile_banner_url from profile where username = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)[0]
    return response


def search_user(search_key):
    """
        Query to search for users from database.

        *Parameters*:
            - *search_key (string)*: part or full user_name or screen_name.

        *Returns*:
            - *response*: a list of dictionary contains search result.
    """
    query: str = """
                         select username, screen_name , profile_image_url from profile
                         where( lower(username) like lower( '%%' || %s || '%%') OR 
                         lower(screen_name) like lower( '%%' || %s || '%%') )
                         
                 """
    data = (search_key, search_key)
    print(data)
    response = db_manager.execute_query(query, data)
    return response


def create_profile(username, screen_name, birth, time):
    """
                                            Query to insert new profile tuple.

                                            *Parameters*:
                                                - *username (string)*: The username attribute in user_profile table .
                                                - *screen_name (string)*: The screen_name attribute in user_profile table .
                                                -*time (date_time)*: the current time
                                            Returns:
                                                - *response*: which is none of case in successful insert .
    """
    query: str = """ 
                        insert into profile(username, screen_name, profile_image_url, profile_banner_url, bio, birth_date, created_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s);
                 """
    data = (username, screen_name, 'profile.jpg', 'banner.png', '', birth, time)
    print(data)
    response = db_manager.execute_query_no_return(query, data)
    return response
