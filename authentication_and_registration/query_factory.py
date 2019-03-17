import database_manager
db_manager = database_manager.db_manager


def is_user(username, password):
    """
    check if the user is on the system.

    *Parameters:*
        -username(str):holds the value of the username.
        -password(str):holds the value of the password.

     *Returns:*
     -*True:* if there is a user.
     -*False:* if there is no user with these info.
    """
    # for testing print username and password
    query: str = """
                     select PASSWORD from USER_CREDENTIALS where USERNAME= %s AND PASSWORD = %s
                 """
    data = (username, password)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    elif response:
        return True
    return False

