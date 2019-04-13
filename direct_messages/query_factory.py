import database_manager

db_manager = database_manager.db_manager


def create_message(from_username, to_username, created_at, text, media_url):
    """
         This function create a message in the database.


         *Parameter:*

             - *from_username*: user who is send the message.
             - *to_username*: user who is received the message.
             - *created_at*: date to be created at which will always be 'datetime.datetime.now()' function.
             - *text*: body of text.
             - *media_url*: url of the media.

         *Returns:*

             - *None*: If the query was executed successfully.
             - *Exception object*: If the query produced an error.
    """
    query: str = """ 
                    INSERT INTO MESSAGE(ID, FROM_USERNAME, TO_USERNAME, CREATED_AT, TEXT, MEDIA_URL)

                    VALUES(DEFAULT, %s, %s, %s, %s, %s)
                """
    data = (from_username, to_username, created_at, text, media_url)
    response = db_manager.execute_query_no_return(query, data)
    return response


def get_messages(from_username, to_username):
    """
             This function retrieve a list of messages from the database.

             *Parameter:*

                 - *from_username*: user who is send the message.
                 - *to_username*: user who is received the message.

             *Returns:*
                - *List of Dictionaries*: {
                                            | *id*: string,
                                            | *created_at*: datetime,
                                            | *from_username*: string,
                                            | *to_username*: string,
                                            | *text*: string,
                                            | *media_url*: string
                                            | }
                 - *Exception object*: If the query produced an error.
    """
    query: str = """
                    SELECT ID, FROM_USERNAME, TO_USERNAME, CREATED_AT, TEXT, MEDIA_URL
                    FROM MESSAGE
                    WHERE FROM_USERNAME = %s
                    AND   TO_USERNAME = %s
                    ORDER BY CREATED_AT DESC 
                 """
    data = (from_username, to_username)
    response = db_manager.execute_query(query, data)
    return response


def get_conversations(auth_username):
    """
             This function retrieve list of conversations with last message .

             *Parameter:*

                 - *auth_username*: user who is send the message.

             *Returns:*

                 - *Dictionary*: {
                                    | *id*: string,
                                    | *created_at*: datetime,
                                    | *from_username*: string,
                                    | *to_username*: string,
                                    | *text*: string,
                                    | *media_url*: string
                                    | *screen_name*: string
                                    | *profile_image_url*: string
                                    | }
                 - *Exception object*: If the query produced an error.
    """
    query: str = """
                    WITH OUTER_GROUP as(			
                                    WITH INNER_GROUP AS(
                                        SELECT SCREEN_NAME, PROFILE_IMAGE_URL, ID, FROM_USERNAME, TO_USERNAME , 
                                        MESSAGE.CREATED_AT, TEXT, MEDIA_URL, 
                                        REPLACE(CONCAT(FROM_USERNAME,TO_USERNAME),%s,'')AS T  
                                        FROM MESSAGE INNER JOIN PROFILE ON USERNAME=TO_USERNAME
                                        WHERE FROM_USERNAME=%s
                                        AND TO_USERNAME IN
                                        (
                                            SELECT DISTINCT TO_USERNAME
                                            FROM MESSAGE
                                            WHERE FROM_USERNAME=%s
                
                                            UNION
                
                                            SELECT DISTINCT FROM_USERNAME
                                            FROM MESSAGE
                                            WHERE TO_USERNAME=%s
                                        )
                
                                        UNION
                
                                        SELECT SCREEN_NAME, PROFILE_IMAGE_URL, ID, FROM_USERNAME, TO_USERNAME , 
                                        MESSAGE.CREATED_AT, TEXT,  MEDIA_URL,
                                        REPLACE(CONCAT(FROM_USERNAME,TO_USERNAME),%s,'')AS T
                                        FROM MESSAGE INNER JOIN PROFILE ON USERNAME=FROM_USERNAME
                                        WHERE TO_USERNAME=%s
                                        AND FROM_USERNAME IN
                                        (
                                            SELECT DISTINCT TO_USERNAME
                                            FROM MESSAGE
                                            WHERE FROM_USERNAME=%s
                
                                            UNION
                
                                            SELECT DISTINCT FROM_USERNAME
                                            FROM MESSAGE
                                            WHERE TO_USERNAME=%s
                                        )
                                    )
	
                    SELECT *,ROW_NUMBER()OVER (PARTITION BY T ORDER BY CREATED_AT DESC) as TEMP
                    FROM INNER_GROUP
	        )

                    SELECT SCREEN_NAME, PROFILE_IMAGE_URL, ID, FROM_USERNAME, TO_USERNAME ,CREATED_AT, TEXT, MEDIA_URL
                    FROM OUTER_GROUP
                    WHERE OUTER_GROUP.TEMP=1
                    ORDER BY CREATED_AT DESC 
                 """
    data = (auth_username,auth_username,auth_username,auth_username,auth_username,
            auth_username,auth_username,auth_username)
    response = db_manager.execute_query(query, data)
    return response


def check_follow(follower, followed):
    """
            This function checks if the user follows another user in the database or not.


            *Parameter:*

                - *follower:* follower user to be checked in the database.
                - *followed:* followed user to be checked in the database.

            *Returns:*
                - a query to be check if exist or not.
        """
    query: str = """
                    SELECT *
                    FROM FOLLOW 
                    WHERE FOLLOWER_USERNAME = %s
                    AND FOLLOWED_USERNAME = %s
                 """
    data = (follower, followed)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def check_block(blocker, blocked):
    """
            This function checks if the user blocked another user in the database or not.


            *Parameter:*

                - *blocker:* blocker user to be checked in the database.
                - *blocked:* blocked user to be checked in the database.

            *Returns:*
                - a query to be check if exist or not.
    """
    query: str = """
                    SELECT *
                    FROM BLOCK 
                    WHERE BLOCKER_USERNAME = %s
                    AND BLOCKED_USERNAME = %s
                 """
    data = (blocker, blocked)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def check_mute(muter, muted):
    """
            This function checks if the user muted another user in the database or not.


            *Parameter:*

                - *muter:* muter user to be checked in the database.
                - *muted:* muted user to be checked in the database.

            *Returns:*
                - a query to be check if exist or not.
    """
    query: str = """
                    SELECT *
                    FROM MUTE 
                    WHERE MUTER_USERNAME = %s
                    AND MUTED_USERNAME = %s
                 """
    data = (muter, muted)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True


def get_recent_conversationers(from_username):
    """
             This function retrieve list of conversationers.

             *Parameter:*

                 - *from_username*: user who is send the message.

             *Returns:*

                 - *Dictionary*: {
                                    | *username*: string,
                                    | *screen_name*: string
                                    | *profile_image_url*: string
                                    | }
                 - *Exception object*: If the query produced an error.
    """

    query: str = """
                    WITH GROUPS AS
                    (
                     SELECT SCREEN_NAME, PROFILE_IMAGE_URL, ID, FROM_USERNAME, TO_USERNAME , MESSAGE.CREATED_AT, TEXT, 
                     MEDIA_URL, row_number() OVER (
                                                    PARTITION BY TO_USERNAME 
                                                    ORDER BY MESSAGE.CREATED_AT DESC
                                                    ) AS TEMP
                     FROM MESSAGE INNER JOIN PROFILE ON USERNAME=TO_USERNAME
                     WHERE FROM_USERNAME  = %s
                    )

                    SELECT SCREEN_NAME, PROFILE_IMAGE_URL,  TO_USERNAME AS USERNAME
                    FROM GROUPS
                    WHERE GROUPS.TEMP=1

                    ORDER BY CREATED_AT DESC ,USERNAME ASC
                 """
    data = (from_username,)
    response = db_manager.execute_query(query, data)
    return response
