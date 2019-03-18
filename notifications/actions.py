from . import query_factory
import datetime
from models import Notification
from timelines_and_trends import actions


def get_notifications(username):
    """
        This function get list of notifications for a given username by converting lists of dictionaries
        into lists of notification model, it call fucntion from query factory that returns lists of
        dictionaries fit notification model.


        *Parameter:*

            - *username*: user who is responsible for the notification.

        *Returns*:

            - *models.Notification object*
        """
    notifications = query_factory.get_notifications(username)
    notifications = actions.paginate(notifications, 2, 'id', 4)
    print(notifications)
    notification_list = []
    if len(notifications) == 0:
        return notification_list
    for notification in notifications:
        notification_list.append(Notification(notification))
    return notification_list


def create_notifications(involved_username, type_notification, kweek_id):
    """
     This function create a notification in the database.


     *Parameter:*

         - *involved_username*: user who is reposonsible for the notification.
         - *type_notification*: type of the notification [FOLLOW-REKWEEK-LIKE].
         - *kweek_id*: the id of the kweek involved.

     *Returns:*

         - *None*: If the query was executed successfully.
         - *Exception* object: If the query produced an error.
     """
    return query_factory.create_notifications(involved_username, type_notification, kweek_id, datetime.datetime.now())


# function for testing
def count_notification():
    """
        This function count all notifications in database.


        *Parameter:*

            - no parameter.

        *Returns:*
            - number of notifications in the database.
    """
    return query_factory.count_notification()


def is_user(username):
    """
        This function checks if the user is in the database or not.


        *Parameter:*

            - *username:* username to be checked in the database.

        *Returns:*
            - a boolean representing if exists in the database or not.
    """
    return query_factory.is_user(username)
