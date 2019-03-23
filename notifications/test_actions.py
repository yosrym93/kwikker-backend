from . import actions
from database_manager import db_manager
import pytest
db_manager.initialize_connection('kwikker', 'postgres', '123456')


@pytest.mark.parametrize("test_username, expected_output, last_notification_retrieved_id",
                         [
                             ('omar', 0, 1),
                             ('khaled', 1, None),
                             ('khaled', 0, 12)
                         ])
def test_get_notifications(test_username, expected_output, last_notification_retrieved_id):
    """
    this function tests if list of notifications is returned properly by checking size of the list
    """

    list_notifications = actions.get_notifications(test_username, last_notification_retrieved_id)
    count = len(list_notifications)
    assert count == expected_output


@pytest.mark.parametrize("involved_username , notified_username, type_notification,"
                         " expected_output, last_notification_retrieved_id",
                         [
                             ('khaled', 'omar', "REKWEEK", True, 1)
                         ])
def test_create_notifications(involved_username, notified_username, type_notification,
                              expected_output, last_notification_retrieved_id):
    """
    this function tests if notification is created in the database by counting number of notification in the database

    """
    old_size = actions.count_notification()
    actions.create_notifications(involved_username, notified_username,
                                 type_notification, last_notification_retrieved_id)
    new_size = actions.count_notification()
    assert new_size > old_size
