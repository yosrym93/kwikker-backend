import database_manager
db_manager = database_manager.db_manager


def get_notifications(involved_username):
    """
            This function get list of notifications for a given username.


            *Parameter:*

                - *username*: user who user who will be notified.

            *Returns*:

                - *List of Dictionaries*: {
                                            | *id*: string,
                                            | *created_at*: datetime,
                                            | *type*: [FOLLOW-REKWEEK-LIKE],
                                            | *username*: string,
                                            | *screen_name*: string,
                                            | *kweek_id*: string,
                                            | *kweek_text*: string,
                                            | *profile_pic_URL*: string
                                            | }
                - *Exception object*: If the query produced an error.
    """
    query: str = """ SELECT NOTIFICATION.ID AS id,NOTIFICATION.CREATED_AT AS created_at,TYPE AS type,
                     NOTIFICATION.INVOLVED_USERNAME AS username,SCREEN_NAME AS screen_name,
                     INVOLVED_KWEEK_ID AS kweek_id,TEXT AS kweek_text, PROFILE_IMAGE_URL AS profile_pic_url 
                      
                     FROM NOTIFICATION INNER JOIN PROFILE ON INVOLVED_USERNAME=USERNAME	  
                     LEFT OUTER JOIN KWEEK ON INVOLVED_KWEEK_ID = KWEEK.ID
                        
                      
                     WHERE NOTIFIED_USERNAME = %s
                      
                     ORDER BY NOTIFICATION.CREATED_AT DESC
                      
                 """

    data = (involved_username,)
    response = db_manager.execute_query(query, data)
    return response


def create_notifications(involved_username, notified_username, type_notification, kweek_id, created_at):
    """
         This function create a notification in the database.


         *Parameter:*

             - *involved_username*: user who is responsible for the notification.
             - *notified_username*: user who is notified.
             - *type_notification*: type of the notification [FOLLOW-REKWEEK-LIKE].
             - *kweek_id*: the id of the kweek involved.
             - *created_at*: date to be created at which will always be 'datetime.datetime.now()' function

         *Returns:*

             - *None*: If the query was executed successfully.
             - *Exception object*: If the query produced an error.
    """
    query: str = """
                    INSERT INTO NOTIFICATION(ID, CREATED_AT, NOTIFIED_USERNAME, INVOLVED_USERNAME, 
                    TYPE, INVOLVED_KWEEK_ID, IS_SEEN)
                     
                    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)
                 """

    data = (created_at, notified_username, involved_username, type_notification, kweek_id, False)
    response = db_manager.execute_query_no_return(query, data)
    return response


# function for testing
def count_notification():
    """
           This function count all notifications in database.


           *Parameter:*

               - no parameter.

           *Returns:*
               - number of notifications in the database.
    """
    query: str = """
                    SELECT COUNT(*) FROM NOTIFICATION
                 """
    response = db_manager.execute_query(query)
    return response


def is_kweek(kweek_id):
    """
                This function checks if the kweek_id is in the database or not.


                *Parameter:*

                    - *kweek_id:* kweek_id to be checked in the database.

                *Returns:*
                    - a query to be check if exist or not.
    """
    query = """
                SELECT * FROM KWEEK WHERE ID = %s
            """
    data = (kweek_id,)
    return db_manager.execute_query(query, data)


def is_notification(involved_username, notified_username, type_notification, kweek_id=None):
    """
                    This function checks if the notification  is in the database or not with this specific parameter.


                    *Parameter:*

                        - *involved_username:* involved_username in the database.
                        - *notified_username:* notified_username in the database.
                        - *type_notification:* type_notification in the database.
                        - *kweek_id:* kweek_id in the database.

                    *Returns:*
                        - a query to be check if exist or not.
        """
    if kweek_id is None:
        query = """
                    SELECT * 
                    
                    FROM NOTIFICATION 
                    
                    WHERE INVOLVED_USERNAME= %s
                    AND   NOTIFIED_USERNAME= %s
                    AND   TYPE= %s
                    AND   INVOLVED_KWEEK_ID IS %s
                    
                    ORDER BY NOTIFICATION.CREATED_AT DESC
                """
    else:
        query = """
                    SELECT * 

                    FROM NOTIFICATION 

                    WHERE INVOLVED_USERNAME= %s
                    AND   NOTIFIED_USERNAME= %s
                    AND   TYPE= %s
                    AND   INVOLVED_KWEEK_ID = %s

                    ORDER BY NOTIFICATION.CREATED_AT DESC
                """
    data = (involved_username, notified_username, type_notification, kweek_id)
    return db_manager.execute_query(query, data)

