from . import actions
import jwt
from database_manager import db_manager
from app import secret_key
import pytest
db_manager.initialize_connection('kwikker', 'postgres', '1')
"""
@pytest.mark.skip(reason="bla bla")  => to skip test
command: pytest -v -rxs
@pytest.mark.skipif(condition ,reason="bla bla")  => to skip test
command: pytest -v -rxs
pytest -v --capture=no => to see functions print for test cases
"""


def test_create_token():
    token = actions.create_token('milan')
    answer = jwt.decode(token, secret_key, algorithms=['HS256'])
    print(answer)
    assert answer['username'] == 'milan'


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
