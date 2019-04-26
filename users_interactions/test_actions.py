from datetime import date, datetime
import pytest
from models import UserProfile, User
from app import app
from . import actions
server_path = app.config['SERVER_PATH']


@pytest.mark.parametrize("test_username, test_last_retrieved_username, test_authorized_username, expected_output", [
                             ('khaled', None, 'khaled',
                              [
                                 UserProfile({
                                    "username": "amr",
                                    "screen_name": "bogy",
                                    "bio": "he is a doll",
                                    "birth_date": date(1998, 3, 23),
                                    "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                    "followers_count": 0,
                                    "following_count": 1,
                                    "kweeks_count": 0,
                                    "likes_count": 0,
                                    "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                    "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                    "following": False,
                                    "follows_you": True,
                                    "blocked": False,
                                    "muted": False
                                 }),
                                 UserProfile({
                                     "username": "omar",
                                     "screen_name": "3moar",
                                     "bio": "he is a late man",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 0,
                                     "following_count": 1,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": False
                                 }),
                                 UserProfile({
                                     "username": "omar@figo",
                                     "screen_name": "omar_figo",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 0,
                                     "following_count": 1,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": False
                                 }),
                              ]),
                             ('khaled', 'omar@figo', 'khaled',
                              [
                                 UserProfile({
                                     "username": "ahmed_khaled",
                                     "screen_name": "@ahmed_khaled",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 0,
                                     "following_count": 1,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": False
                                 }),
                                 UserProfile({
                                     "username": "ahmed",
                                     "screen_name": "mido",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 0,
                                     "following_count": 1,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": False
                                 }),
                                 UserProfile({
                                     "username": "yosry",
                                     "screen_name": "@yosry",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 0,
                                     "following_count": 1,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": False
                                 }),
                              ]),
                             ('khaled', "", 'Khaled', None)
])
def test_get_profile_followers(test_username, test_last_retrieved_username, test_authorized_username, expected_output):
    output = actions.get_profile_followers(test_username, test_last_retrieved_username, test_authorized_username)
    new_output = []
    new_expected_output = []
    if output is not None:
        for x in output:
            z = x.to_json()
            new_output.append(z)
    if expected_output is not None:
        for x in expected_output:
            z = x.to_json()
            new_expected_output.append(z)
    assert new_output == new_expected_output


@pytest.mark.parametrize("test_username, test_last_retrieved_username, test_authorized_username, expected_output", [
                             ('khaled', None, 'khaled',
                              [
                                 UserProfile({
                                     "username": "khaled ahmed",
                                     "screen_name": "screen_name1",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 1,
                                     "following_count": 0,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": True,
                                     "follows_you": False,
                                     "blocked": False,
                                     "muted": False
                                 }),
                                 UserProfile({
                                     "username": "khaled mohamed",
                                     "screen_name": "screen_name1",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 1,
                                     "following_count": 0,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": True,
                                     "follows_you": False,
                                     "blocked": False,
                                     "muted": False
                                 }),
                                 UserProfile({
                                     "username": "mohamed khaled",
                                     "screen_name": "screen_name1",
                                     "bio": "",
                                     "birth_date": date(1998, 3, 23),
                                     "created_at": datetime(2006, 12, 19, 10, 10, 24),
                                     "followers_count": 1,
                                     "following_count": 0,
                                     "kweeks_count": 0,
                                     "likes_count": 0,
                                     "profile_banner_url": server_path + "user/upload/banner/banner.png",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": True,
                                     "follows_you": False,
                                     "blocked": False,
                                     "muted": False
                                 }),
                              ]),
                             ('khaled', "", 'Khaled', None),
                             ('khaled', 'mohamed khaled', 'khaled', []),
])
def test_get_profile_following(test_username, test_last_retrieved_username, test_authorized_username, expected_output):
    output = actions.get_profile_following(test_username, test_last_retrieved_username, test_authorized_username)
    new_output = []
    new_expected_output = []
    if output is not None:
        for x in output:
            z = x.to_json()
            new_output.append(z)
    if expected_output is not None:
        for x in expected_output:
            z = x.to_json()
            new_expected_output.append(z)
    assert new_output == new_expected_output


@pytest.mark.parametrize("test_authorized_username,test_username, expected_output",
                         [
                             ('khaled', 'amr', None),
                             ('khaled', 'amr', 'user already muted'),
                             ('khaled', 'omar', None),
                         ])
def test_mute(test_authorized_username, test_username, expected_output):
    output = actions.mute(test_authorized_username, test_username)
    assert output == expected_output


@pytest.mark.parametrize("test_authorized_username,expected_output", [
                          ('khaled',
                           [
                                 User({
                                    "username": "amr",
                                    "screen_name": "bogy",
                                    "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                    "following": False,
                                    "follows_you": True,
                                    "blocked": False,
                                    "muted": True
                                 }),
                                 User({
                                     "username": "omar",
                                     "screen_name": "3moar",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": True,
                                     "blocked": False,
                                     "muted": True
                                 })
                           ]),
                          ('amr', []),

])
def test_get_muted_users(test_authorized_username, expected_output):
    output = actions.get_muted_users(test_authorized_username)
    new_output = []
    new_expected_output = []
    if output is not None:
        for x in output:
            z = x.to_json()
            new_output.append(z)
    if expected_output is not None:
        for x in expected_output:
            z = x.to_json()
            new_expected_output.append(z)
    assert new_output == new_expected_output


@pytest.mark.parametrize("test_authorized_username,test_username, expected_output",
                         [
                             ('khaled', 'amr', None),
                             ('khaled', 'amr', 'user already unmuted'),
                         ])
def test_unmute(test_authorized_username, test_username, expected_output):
    output = actions.unmute(test_authorized_username, test_username)
    assert output == expected_output


@pytest.mark.parametrize("test_authorized_username,test_username, expected_output",
                         [
                             ('khaled', 'amr', None),
                             ('khaled', 'amr', 'user already blocked'),
                             ('khaled', 'omar', None)
                         ])
def test_block(test_authorized_username, test_username, expected_output):
    output = actions.block(test_authorized_username, test_username)
    assert output == expected_output


@pytest.mark.parametrize("test_authorized_username,expected_output", [
                          ('khaled',
                           [
                                 User({
                                    "username": "amr",
                                    "screen_name": "bogy",
                                    "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                    "following": False,
                                    "follows_you": False,
                                    "blocked": True,
                                    "muted": False
                                 }),
                                 User({
                                     "username": "omar",
                                     "screen_name": "3moar",
                                     "profile_image_url": server_path + "user/upload/picture/profile.jpg",
                                     "following": False,
                                     "follows_you": False,
                                     "blocked": True,
                                     "muted": True
                                 })
                           ]),
                          ('amr', []),

])
def test_get_blocked_users(test_authorized_username, expected_output):
    output = actions.get_blocked_users(test_authorized_username)
    new_output = []
    new_expected_output = []
    if output is not None:
        for x in output:
            z = x.to_json()
            new_output.append(z)
    if expected_output is not None:
        for x in expected_output:
            z = x.to_json()
            new_expected_output.append(z)
    assert new_output == new_expected_output


@pytest.mark.parametrize("test_authorized_username,test_username, expected_output",
                         [
                             ('khaled', 'amr', None),
                             ('khaled', 'amr', 'user already unblocked')
                         ])
def test_unblock(test_authorized_username, test_username, expected_output):
    output = actions.unblock(test_authorized_username, test_username)
    assert output == expected_output


@pytest.mark.parametrize("test_username,test_authorized_username, expected_output",
                         [
                             ('khaled', 'amr', None),
                             ('khaled', 'amr', 'you already following that user.'),
                             ('khaled', 'omar', 'you can not follow this user you have been blocked by him.'),
                             ('omar', 'khaled', 'you can not follow this account you have been blocked this account, to follow un block him.')

                         ])
def test_follow(test_username, test_authorized_username,  expected_output):
    output = actions.follow(test_username, test_authorized_username)
    assert output == expected_output


@pytest.mark.parametrize("test_username,test_authorized_username, expected_output",
                         [
                             ('khaled', 'omar', 'you already not following that user'),
                             ('khaled', 'omar@figo', None),
                         ])
def test_unfollow(test_username, test_authorized_username,  expected_output):
    output = actions.unfollow(test_username, test_authorized_username)
    re = actions.get_profile_following('amr', None, 'khaled')
    print(re)
    assert output == expected_output
