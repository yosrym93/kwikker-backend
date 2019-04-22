from datetime import date, datetime
import pytest
import os
import shutil
from models import UserProfile, User
from app import app
from . import actions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
server_path = app.config['SERVER_PATH']


@pytest.mark.parametrize("test_authorized_username, test_username, expected_output",

                         [
                             ('khaled', 'omar', UserProfile({"username": "omar",
                                                             "screen_name": "3moar",
                                                             "bio": "he is a late man",
                                                             "birth_date": date(1998, 3, 23),
                                                             "created_at": datetime(2001, 12, 19, 10, 10, 24),
                                                             "followers_count": 1,
                                                             "following_count": 2,
                                                             "kweeks_count": 1,
                                                             "likes_count": 1,
                                                             "profile_banner_url": server_path + "user/upload"
                                                                                   "/banner/banne.png",
                                                             "profile_image_url": server_path + "user/upload"
                                                                                  "/picture/profil.jpg",
                                                             "following": False,
                                                             "follows_you": True,
                                                             "blocked": False,
                                                             "muted": False
                                                             })),
                             ('khaled', 'amr', UserProfile({"username": "amr",
                                                            "screen_name": "bogy",
                                                            "bio": "he is a doll",
                                                            "birth_date": date(1998, 3, 23),
                                                            "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                                            "followers_count": 1,
                                                            "following_count": 2,
                                                            "kweeks_count": 1,
                                                            "likes_count": 2,
                                                            "profile_banner_url": server_path + "user"
                                                                                  "/upload/banner/banner.png",
                                                            "profile_image_url": server_path + "user/upload"
                                                                                 "/picture/profile.jpg",
                                                            "following": False,
                                                            "follows_you": True,
                                                            "blocked": False,
                                                            "muted": False
                                                            })),
                             ('omar', 'khaled', UserProfile({"username": "khaled",
                                                             "screen_name": "gellesh",
                                                             "bio": "he is a man",
                                                             "birth_date": date(1998, 12, 23),
                                                             "created_at": datetime(2004, 10, 19, 10, 23, 54),
                                                             "followers_count": 2,
                                                             "following_count": 0,
                                                             "kweeks_count": 3,
                                                             "likes_count": 3,
                                                             "profile_banner_url": server_path + "user"
                                                                                   "/upload/banner/khaledbanner.jpg",
                                                             "profile_image_url": server_path + "user/upload"
                                                                                  "/picture/khaledprofile.jpg",
                                                             "following": True,
                                                             "follows_you": False,
                                                             "blocked": False,
                                                             "muted": False
                                                             })),
                             ('omar', 'k', -1),
                             ('khaled', None, - 1)
                         ]
                         )
def test_get_user_profile(test_authorized_username, test_username, expected_output):
    output = actions.get_user_profile(test_authorized_username, test_username)
    if output == -1 or output == 'k':
        assert output == expected_output
    else:
        assert output.to_json() == expected_output.to_json()


@pytest.mark.parametrize("test_authorized_username,test_bio,test_screen_name,expected_output",

                         [
                             ('khaled', 'test bio', 'test screen_name', None),
                             ('khaled', '', 'test screen_name2', None),
                             ('khaled', 'test bio2', '', None),
                             ('khaled', '', '', 0),
                             ('khaled', None, 'test screen_name2', None),
                             ('khaled', 'test bio2', None, None),
                             ('khaled', None, None, 0)
                         ])
def test_update_user_profile(test_authorized_username, test_bio, test_screen_name, expected_output):
    output = actions.update_user_profile(test_authorized_username, test_bio, test_screen_name)
    assert output == expected_output


@pytest.mark.parametrize("test_authorized_username,expected_output",
                         [
                             ('khaled', server_path + 'user/upload/picture/profile.jpg'),
                             ('amr', 'default image'),
                             ('omar', 'file does not exist')

                         ])
def test_delete_profile_picture(test_authorized_username, expected_output):
    if test_authorized_username == 'khaled':
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_profile = path + '/images/test/khaledprofile.jpg'
        destination_profile = path + '/images/profile'
        os.chdir(os.path.dirname(path))
        shutil.copy(source_profile, destination_profile)
    output = actions.delete_profile_picture(test_authorized_username)
    assert output == expected_output


@pytest.mark.parametrize("test_authorized_username,expected_output",
                         [
                             ('khaled', server_path + 'user/upload/banner/banner.png'),
                             ('amr', 'default image'),
                             ('omar', 'file does not exist')
                         ])
def test_delete_profile_banner(test_authorized_username, expected_output):
    if test_authorized_username == 'khaled':
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        source_banner = path + '/images/test/khaledbanner.jpg'
        destination_banner = path + '/images/banner'
        os.chdir(os.path.dirname(path))
        shutil.copy(source_banner, destination_banner)
    output = actions.delete_banner_picture(test_authorized_username)
    assert output == expected_output


@pytest.mark.parametrize("test_upload_type, test_filename, expected_output",
                         [
                             (
                                     'picture', 'khaledprofile.png',
                                     server_path + 'user/upload/picture/khaledprofile.png'),
                             (
                                     'picture', 'omarprofile.png',
                                     server_path + 'user/upload/picture/omarprofile.png'),
                             (
                                     'banner', 'khaledbanner.png',
                                     server_path + 'user/upload/banner/khaledbanner.png')
                         ])
def test_create_url(test_upload_type, test_filename, expected_output):
    output = actions.create_url(test_upload_type, test_filename)
    assert output == expected_output


@pytest.mark.parametrize("test_filename, expected_output",
                         [
                             ('khaledprofile.png', True),
                             ('omarprofile.jpg', True),
                             ('khaledbanner.jpeg', True),
                             ('khaledbanner.jpeg', True),
                             ('khaledbanner.pdf', False),
                             ('khaledbanner.zip', False),
                         ])
def test_allowed_file(test_filename, expected_output):
    output = actions.allowed_file(test_filename)
    assert output == expected_output


@pytest.mark.parametrize("test_username, test_screen_name, test_birth_date, expected_output",
                         [
                             ('khaled', 'khaled', '2001-03-12', False),
                             ('', 'med7at', '2001-03-12', False),
                             ('ahmed', 'a7med', '2001-03-12', True),
                             ('yosry', 'Yosry86', '2001-03-12', True),
                         ])
def test_create_profile(test_username, test_screen_name, test_birth_date, expected_output):
    output = actions.create_profile(test_username, test_screen_name, test_birth_date)
    assert output == expected_output

"""
@pytest.mark.parametrize("test_authorized_username, test_search_key, test_username, expected_output",
                         [
                             ('khaled', 'KhAlEd', None, [
                                 User({"username": "khaled ahmed",
                                       "screen_name": "screen_name1",
                                       "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                       "following": False,
                                       "follows_you": False,
                                       "blocked": False,
                                       "muted": False
                                       }),
                                 User({"username": "khaled mohamed",
                                       "screen_name": "screen_name1",
                                       "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                       "following": False,
                                       "follows_you": False,
                                       "blocked": False,
                                       "muted": False
                                       }),
                                 User({"username": "mohamed khaled",
                                       "screen_name": "screen_name1",
                                       "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                       "following": False,
                                       "follows_you": False,
                                       "blocked": False,
                                       "muted": False
                                       }),
                                 User({"username": "KHALED_AMR",
                                       "screen_name": "screen_name1",
                                       "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                       "following": False,
                                       "follows_you": False,
                                       "blocked": False,
                                       "muted": False
                                       }),
                                 User({"username": "omar_khaled",
                                       "screen_name": "screen_name1",
                                       "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                       "following": False,
                                       "follows_you": False,
                                       "blocked": False,
                                       "muted": False
                                       }),
                             ]),

                             ('khaled', 'KhaLeD', 'amykhaledradawn', [
                                User({"username": "ramy_khaled_amr",
                                      "screen_name": "screen_name1",
                                      "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                      "following": False,
                                      "follows_you": False,
                                      "blocked": False,
                                      "muted": False
                                      }),
                                User({"username": "ahmed_khaled",
                                      "screen_name": "screen_name1",
                                      "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                      "following": False,
                                      "follows_you": False,
                                      "blocked": False,
                                      "muted": False
                                      }),
                                User({"username": "khaled",
                                      "screen_name": "test screen_name2",
                                      "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                      "following": None,
                                      "follows_you": None,
                                      "blocked": None,
                                      "muted": None
                                      }),
                             ]),
                             ('khaled', '', 'sss', []),
                             ('khaled', 'amr', 'ramy_khaled_amr', []),
                         ])
def test_search_user(test_authorized_username, test_search_key, test_username, expected_output):
    output = actions.search_user(test_authorized_username, test_search_key, test_username)
    new_output = []
    new_expected_output = []
    for x in output:
        z = x.to_json()
        new_output.append(z)
    for x in expected_output:
        z = x.to_json()
        new_expected_output.append(z)
    assert new_output == new_expected_output
"""