from . import query_factory
import datetime
"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def get_notifications(username):
    return query_factory.get_notifications(username)


def create_notifications(involved_username, type_notification, kweek_id):
    return query_factory.create_notifications(involved_username, type_notification, kweek_id, datetime.datetime.now())


# function for testing
def get_list_size_notification():
    return query_factory.get_list_size_notification()
