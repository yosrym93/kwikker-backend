from . import actions
from database_manager import db_manager
import pytest


def get_id(from_username, to_username):
    query = """     SELECT ID, FROM_USERNAME, TO_USERNAME, CREATED_AT, TEXT, MEDIA_URL
                    FROM MESSAGE
                    WHERE FROM_USERNAME = %s
                    AND   TO_USERNAME = %s
                    
                    UNION
                    
                    SELECT ID, FROM_USERNAME, TO_USERNAME, CREATED_AT, TEXT, MEDIA_URL
                    FROM MESSAGE
                    WHERE FROM_USERNAME = %s
                    AND   TO_USERNAME = %s
                    
                    ORDER BY CREATED_AT DESC
                    LIMIT 1
            """
    data = (from_username, to_username, to_username, from_username)
    last_id = db_manager.execute_query(query, data)[0]['id']
    return last_id


def count_message(from_username, to_username):
    return len(actions.get_messages(from_username, to_username))


@pytest.mark.parametrize("test_username, expected_output, last_conversations_retrieved_id",
                         [
                             ('ahly', 3, None),
                         ])
def test_get_conversations(test_username, expected_output, last_conversations_retrieved_id):
    """
        this function tests if list of conversations is returned properly by checking size of the list
    """
    list_conversations = actions.get_conversations(test_username, last_conversations_retrieved_id)
    count = len(list_conversations)
    assert count == expected_output


def test_get_conversations_value_error():
    """
        this function tests exception error of value
    """
    exception_caught = False
    try:
        actions.get_conversations('ahly', 'invalid_id')
    except ValueError:
        exception_caught = True
    assert exception_caught is True


def test_get_conversations_empty():
    """
        this function tests exception when conversations return empty list
    """
    list_conversations = actions.get_conversations('no_message', None)
    assert list_conversations == []


@pytest.mark.parametrize("from_username, to_username, expected_output, last_message_retrieved_id",
                         [
                             ('ahly', 'zamalek', 2, None),
                             ('ahly', 'zamalek', 1, get_id('ahly', 'zamalek')),
                         ])
def test_get_messages(from_username, to_username, expected_output, last_message_retrieved_id):
    """
        this function tests if list of messages is returned properly by checking size of the list
    """
    list_messages = actions.get_messages(from_username, to_username, last_message_retrieved_id)
    count = len(list_messages)
    assert count == expected_output


def test_get_messages_value_error():
    """
        this function tests exception error of value
    """
    exception_caught = False
    try:
        actions.get_messages('ahly', 'zamalek', 'invalid_id')
    except ValueError:
        exception_caught = True
    assert exception_caught is True


def test_get_messages_empty():
    """
        this function tests exception when messages return empty list
    """
    list_messages = actions.get_messages('no_message', 'zamalek', None)
    assert list_messages == []


def test_create_message():
    """
        this function tests if list of messages is created properly by checking size of the list
    """
    old_size = count_message('ahly', 'zamalek')
    actions.create_message('ahly', 'zamalek', 'test message', None)
    new_size = count_message('ahly', 'zamalek')
    assert new_size == (old_size + 1)


def test_create_message_from_user_error():
    """
        this function tests exception error of involved_user
    """
    try:
        actions.create_message('qq', 'zamalek', 'test message', None)
    except Exception as E:
        assert str(E) == 'Username who sent this message does not exist.'


def test_create_message_to_user_error():
    """
        this function tests exception error of notified_user
    """
    try:
        actions.create_message('zamalek', 'qq', 'test message', None)
    except Exception as E:
        assert str(E) == 'Username who want to receive this message does not exist.'


@pytest.mark.parametrize("test_username, expected_output, last_conversationers_retrieved_username",
                         [
                             ('ahly', 3, None)
                         ])
def test_get_conversationers(test_username, expected_output, last_conversationers_retrieved_username):
    """
        this function tests if list of conversations is returned properly by checking size of the list
    """
    list_conversationers = actions.get_recent_conversationers(test_username, last_conversationers_retrieved_username)
    count = len(list_conversationers)
    assert count == expected_output


def test_get_conversationers_not_exist():
    """
        this function tests if list of conversations is returned properly by checking size of the list
    """
    try:
        actions.get_recent_conversationers('ahly', 'qq')
    except Exception as E:
        assert str(E) == 'Username does not exist.'


def test_get_conversationers_empty():
    """
        this function tests exception when conversations return empty list
    """
    list_conversations = actions.get_recent_conversationers('no_message', None)
    assert list_conversations == []


def test_get_conversationers_user():
    """
        this function tests exception when conversations return empty list
    """
    list_conversations = actions.get_recent_conversationers('ahly', 'no_message')
    assert list_conversations == []
