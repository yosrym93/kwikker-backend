from . import actions
from database_manager import db_manager
import pytest


def get_id(notified_username, involved_username, notif_type):
    query = "SELECT id FROM NOTIFICATION WHERE notified_username=%s AND involved_username=%s AND type=%s"
    data = (notified_username, involved_username, notif_type)
    kweek_id = db_manager.execute_query(query, data)[0]['id']
    return kweek_id


@pytest.mark.parametrize("test_username, expected_output, last_notification_retrieved_id",
                         [
                             ('zamalek', 1, None),
                             ('zamalek', 0, get_id('zamalek', 'degla', 'FOLLOW'))
                         ])
def test_get_notifications(test_username, expected_output, last_notification_retrieved_id):
    """
    this function tests if list of notifications is returned properly by checking size of the list
    """
    list_notifications = actions.get_notifications(test_username, last_notification_retrieved_id)
    count = len(list_notifications)
    assert count == expected_output


def test_get_notifications_empty():
    """
        this function tests exception when notification return empty list
    """
    list_notifications = actions.get_notifications('arsenal', None)
    assert list_notifications == []


def test_get_notifications_value_error():
    """
        this function tests exception error of value
    """
    exception_caught = False
    try:
        actions.get_notifications('ahly', 'invalid_id')
    except ValueError:
        exception_caught = True
    assert exception_caught is True


def test_create_notifications_type_error():
    """
        this function tests exception error of type of notification
    """
    try:
        actions.create_notifications('ahly', 'zamalek', 'ASA')
    except Exception as E:
        assert str(E) == 'Type does not exist'


def test_create_notifications_i_user_error():
    """
        this function tests exception error of involved_user
    """
    try:
        actions.create_notifications('qq', 'zamalek', 'FOLLOW')
    except Exception as E:
        assert str(E) == 'Involved_username does not exist'


def test_create_notifications_n_user_error():
    """
        this function tests exception error of notified_user
    """
    try:
        actions.create_notifications('zamlek', 'qq', 'FOLLOW')
    except Exception as E:
        assert str(E) == 'Involved_username does not exist'


def test_create_notifications_kweek_id_error():
    """
        this function tests exception error of kweek id
    """
    try:
        actions.create_notifications('zamlek', 'qq', 'FOLLOW', 99999999)
    except Exception as E:
        assert str(E) == 'A kweek with this username does not exist'


@pytest.mark.parametrize("involved_username , notified_username, type_notification,"
                         " expected_output, last_notification_retrieved_id",
                         [
                             ('ahly', 'degla', "FOLLOW", True, None),
                             ('ahly', 'degla', "FOLLOW", False, None)
                         ])
def test_create_notifications(involved_username, notified_username, type_notification,
                              expected_output, last_notification_retrieved_id):
    """
    this function tests if notification is created in the database by counting number of notification in the database

    """
    output = False
    old_size = actions.count_notification()
    actions.create_notifications(involved_username, notified_username,
                                 type_notification, last_notification_retrieved_id)
    new_size = actions.count_notification()
    if new_size > old_size:
        output = True
    assert expected_output == output


def test_is_kweek_not_exits():
    """
        this function tests if kweek with given id doesn't exist

    """
    expected_output = actions.is_kweek(999999999999999)
    assert expected_output is False


def test_is_kweek_exists():
    """
        this function tests if kweek with given id exist

    """
    query = "SELECT id FROM KWEEK WHERE username='ahly'"
    kweek_id = db_manager.execute_query(query)[0]['id']
    expected_output = actions.is_kweek(kweek_id)
    assert expected_output is True
