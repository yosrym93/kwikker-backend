import database_manager

db_manager = database_manager.db_manager

"""
    Create your functions here that contain only query construction logic.
    When passing parameters to queries use the method shown here:
    http://initd.org/psycopg/docs/usage.html

    Never use string concatenation or any other string formatting methods other than the one specified.

    You must check that the returned object is not an exception.

    The return of a SELECT query is a list of dictionaries, where each row is represented by a dictionary.
    The keys of the dictionary are the database column names.
"""


def get_notifications(user):
    query: str = """SELECT  NOTIFICATION.ID AS id,NOTIFICATION.CREATED_AT AS created_at,TYPE AS type,
    PROFILE.USERNAME AS username,SCREEN_NAME AS screen_name,INVOLVED_KWEEK_ID AS kweek_id,TEXT AS kweek_text,
    PROFILE_IMAGE_URL AS profile_pic_url FROM NOTIFICATION INNER JOIN USER_CREDENTIALS 
    ON NOTIFIED_USERNAME=USERNAME INNER JOIN PROFILE ON PROFILE.USERNAME=USER_CREDENTIALS.USERNAME 
    INNER JOIN KWEEK ON INVOLVED_KWEEK_ID = KWEEK.ID where profile.username = %s LIMIT 20"""
    data = (user,)
    response = db_manager.execute_query(query, data)
    return response


def create_notifications(involved_username, type_notification, kweek_id, created_at):
    query: str = """ SELECT  USERNAME  FROM KWEEK WHERE ID = %s"""
    data = (kweek_id,)
    notified_username = db_manager.execute_query(query, data)[0]['username']
    query: str = """INSERT INTO NOTIFICATION(ID, CREATED_AT, NOTIFIED_USERNAME, INVOLVED_USERNAME, 
    TYPE, INVOLVED_KWEEK_ID, IS_SEEN) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"""

    data = (created_at, notified_username, involved_username, type_notification, kweek_id, False)
    response = db_manager.execute_query_no_return(query, data)

    return response


# function for testing
def get_list_size_notification():
    query: str = """SELECT COUNT(*) FROM NOTIFICATION"""
    response = db_manager.execute_query(query)
    return response


def is_user(username):
    query = """
                SELECT * FROM USER_CREDENTIALS WHERE USERNAME = %s
            """
    data = (username,)
    if not db_manager.execute_query(query, data):
        return False
    else:
        return True
