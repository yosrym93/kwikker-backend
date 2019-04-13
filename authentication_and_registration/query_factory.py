import database_manager
import bcrypt
db_manager = database_manager.db_manager


def get_user_by_email(email):
    """
        get specific user by his/her email.

        *Parameters: *
            - * email(string) *: holds the value of the email.


        *Returns: *
            - * user: *if it was found.
            - * False: *if not found.
    """
    query: str = """
                SELECT * FROM USER_CREDENTIALS WHERE EMAIL = %s
                 """
    data = (email,)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    elif response:
        return response[0]


def get_user_by_username(username):
    """
        get specific user by his/her username.

        *Parameters: *
            - * email(string) *: holds the value of the email.


        *Returns: *
            - * user: *if it was found.
            - * False: *if not found.
    """
    query: str = """
                SELECT * FROM USER_CREDENTIALS WHERE USERNAME = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    elif response:
        return response[0]


def username_exists(username):
    """
        check if the username is on the system.

        *Parameters: *
            - * username(string) *: holds the value of the username.


        *Returns: *
            - * True: *if it was found.
            - * False: *if not found.
    """
    query: str = """
                SELECT USERNAME FROM USER_CREDENTIALS WHERE USERNAME = %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    elif response:
        return True
    return False


def email_exists(email):
    """
        check if the email is on the system.

        *Parameters:*
            -*email(string)*:holds the value of the email.

         *Returns:*
         -*True:* if it was found.
         -*False:* if not found.
    """
    query: str = """
                            SELECT * FROM USER_CREDENTIALS WHERE EMAIL=%s
                 """
    data = (email,)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    if response:
        return True
    return False


def add_user(username, password, email):
    """
        Add a user into the system.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*password(string)*:holds the value of the password.
            -*email(string)*:holds the value of email.

         *Returns:*
         -*True:* user added successfully.
         -*False:* error happened.
    """
    query: str = """
                     INSERT INTO USER_CREDENTIALS(USERNAME, PASSWORD, EMAIL, IS_CONFIRMED)
                     VALUES (%s,%s,%s,FALSE)
                 """
    data = (username, password, email)
    db_manager.execute_query_no_return(query, data)


def update_user_password(username, new_password):
    """
        update password of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_password(string)*:holds the value of the new password

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    query: str = """
                     update USER_CREDENTIALS
                     set password = %s
                     where username = %s
                 """
    data = (new_password, username)
    response = db_manager.execute_query_no_return(query, data)
    if type(response) == Exception:
        return False
    else:
        return True


def update_user_username(username, new_username):
    """
        update username of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_username(string)*:holds the value of the new username

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    query: str = """
                     update USER_CREDENTIALS
                     set username = %s
                     where username = %s
                 """
    data = (new_username, username)
    response = db_manager.execute_query_no_return(query, data)
    if type(response) == Exception:
        print('false')
        return False
    else:
        print('true')
        return True


def update_user_email(username, new_email):
    """
        update the email of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_email(string)*:holds the value of the new email

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    query: str = """
                     update USER_CREDENTIALS
                     set email = %s
                     where username = %s
                 """
    data = (new_email, username)
    response = db_manager.execute_query_no_return(query, data)
    if type(response) == Exception:
        return False
    else:
        return True


def confirm_user(username):
    """
        confirm user in the system with thee given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    query: str = """
                     update USER_CREDENTIALS
                     set is_confirmed = True
                     where username = %s
                 """
    data = (username,)
    response = db_manager.execute_query_no_return(query, data)
    if type(response) == Exception:
        return False
    elif response is None:
        return True


def is_user(username, password):
    """
    check if the user is on the system.

    *Parameters:*
        -*username(string)*:holds the value of the username.
        -*password(string)*:holds the value of the password.

     *Returns:*
     -*True:* if there is a user.
     -*False:* if there is no user with these info.
    """
    # for testing print username and password
    query: str = """
                     select PASSWORD from USER_CREDENTIALS where USERNAME= %s
                 """
    data = (username,)
    response = db_manager.execute_query(query, data)
    if type(response) == Exception:
        return False
    elif response:
        # Check that an un-hashed password matches one that has previously been hashed
        if not bcrypt.checkpw(password.encode('utf-8'), response[0]['password'].encode('utf-8')):
            return False
        return True
    return False
