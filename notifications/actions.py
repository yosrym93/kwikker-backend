from . import query_factory
import datetime
"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def get_notifications(username):
    """
        this function get list of notifications for a give username

        **PARAMETER**:

            * *involved_username*: user who is reposonsible for the notification
            * *type_notification*: type of the notification [FOLLOW-REKWEEK-LIKE]
            * *kweek_id*: the id of the kweek involved

        **RETURNS**:

            - list of notifications for the users in json format



        """
    return query_factory.get_notifications(username)


def create_notifications(involved_username, type_notification, kweek_id):
    """
     this function create a notification in the database.

     **PARAMETER**:

         * *involved_username*: user who is reposonsible for the notification
         * *type_notification*: type of the notification [FOLLOW-REKWEEK-LIKE]
         * *kweek_id*: the id of the kweek involved

     **RETURNS**:

         - doesn't return anything


     """
    return query_factory.create_notifications(involved_username, type_notification, kweek_id, datetime.datetime.now())


# function for testing
def get_list_size_notification():
    """
        this function count all notifications in database

        **PARAMETER**:

            - no parameter

        **RETURNS**:
            - number of notifications in the database


        """
    return query_factory.get_list_size_notification()
