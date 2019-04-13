from . import actions
import jwt
from database_manager import db_manager
from app import secret_key, code
import pytest


def test_confirm_user():
    assert actions.confirm_user('milan') is True


def test_create_token():
    token = actions.create_token('milan', 'acm', secret_key)
    answer = jwt.decode(token, secret_key, algorithms=['HS256'])
    assert answer['username'] == 'milan'


def test_create_code():
    token = actions.create_token('milan', 'acm', code)
    answer = jwt.decode(token, code, algorithms=['HS256'])
    assert answer['username'] == 'milan'


@pytest.mark.parametrize("test_email, test_username,expected_output",
                         [
                             ('acm@gmail.com', 'milan', True),
                             ('acm@gmail.com', 'asf', False),
                         ]
                         )
def test_get_user_by_email(test_email, test_username, expected_output):
    user = actions.get_user_by_email(test_email)
    assert (user['username'] == test_username) == expected_output


@pytest.mark.parametrize("test_username, test_email, expected_output",
                         [
                             ('milan', 'acm@gmail.com', True),
                             ('milan', 'asaf', False),
                         ]
                         )
def test_get_user_by_username(test_username, test_email, expected_output):
    user = actions.get_user_by_username(test_username)
    assert (user['email'] == test_email) == expected_output


# you need to delete the user before restarting this unit test
@pytest.mark.parametrize("test_username, test_password, test_email, expected_output_username, expected_output_email",
                         [
                             ('mil', 'aaa', 'acm@gmail.com', False, True),
                             ('milan', 'aaa', 'asaf', True, False),
                             ('amr', 'a', 'amr.ahmed.abdelbaqi@gmail.com', False, False)
                         ]
                         )
def test_add_user(test_username, test_password, test_email, expected_output_username, expected_output_email):
    assert (actions.add_user(test_username, test_password, test_email)) == (expected_output_username,
                                                                            expected_output_email)


@pytest.mark.parametrize("test_username, test_password, expected_output",
                         [
                             ('milan', 'acm', True),
                             ('mil', 'acm', False),
                             ('milan', 'a', False)
                         ]
                         )
def test_verify(test_username, test_password, expected_output):
    answer = actions.verify(test_username, test_password)
    assert answer is expected_output


def test_update_user_password():
    answer = actions.update_user_password('milan', 'aass')
    assert answer is True


@pytest.mark.parametrize("test_username, test_new_email, expected_output",
                         [
                             ('milan', 'acm@gmail.com', False),
                             ('milan', 'acmm@gmail.com', True)
                         ]
                         )
def test_update_user_email(test_username, test_new_email, expected_output):
    answer = actions.update_user_email(test_username, test_new_email)
    assert answer is expected_output


@pytest.mark.parametrize("test_username, test_new_username, expected_output",
                         [
                             ('milan', 'milan', False),
                             ('milan', 'milann', True)
                         ]
                         )
def test_update_user_username(test_username, test_new_username, expected_output):
    answer = actions.update_user_username(test_username, test_new_username)
    assert answer is expected_output
