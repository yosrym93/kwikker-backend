import pytest
from app import app
from . import actions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
Server_path = app.config['SERVER_PATH']

@pytest.mark.parametrize("test_filename, expected_output",
                         [
                             ('20190425223729553712',Server_path + 'media/get/20190425223729553712.png'),
                             ('1287634187234',None),
                             (None,None),


                         ])
def test_create_url(test_filename, expected_output):
    output = actions.create_url(test_filename)
    assert output == expected_output


@pytest.mark.parametrize("test_filename, expected_output",
                         [
                             ('20190425223729553712.png',True),
                             ('20190425223729553712.pdf', False),
                         ])
def test_allowed_file(test_filename, expected_output):
    output = actions.allowed_file(test_filename)
    assert output == expected_output
