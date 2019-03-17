"""
    Your unit tests should reside here.
"""
from . import actions, query_factory
import pytest
import jwt
secretKey = 'amr'
"""
@pytest.mark.skip(reason="bla bla")  => to skip test
command: pytest -v -rxs
@pytest.mark.skipif(condition ,reason="bla bla")  => to skip test
command: pytest -v -rxs
"""


def test_create_token():
    token = actions.create_token('amr')
    answer = jwt.decode(token, secretKey)
    assert answer['username'] == 'amr'


def test_is_user():
    # correct username and password
    answer = query_factory.is_user('amr', 'amrrr')
    assert answer is True
    # invalid username and correct password
    answer = query_factory.is_user('ar', 'amrrr')
    assert answer is False
    # correct username and invalid password
    answer = query_factory.is_user('amr', 'am')
    assert answer is False


def test_verify():
    # account is verified
    answer = actions.verify('amr', 'amrrr')
    assert answer is True
    # account is not verified
    answer = actions.verify('mr', 'amrrr')
    assert answer is False

