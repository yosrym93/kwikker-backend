import pytest
from . import actions
from database_manager import db_manager
from models import User, Mention, Hashtag, Kweek, RekweekInfo
from datetime import datetime

db_manager.initialize_connection('kwikker', 'postgres', '')


@pytest.mark.parametrize("authorized_username, required_username, expected_output",
                         [
                            ('test_user1', 'test_user2', {
                                 'following': False,
                                 'follows_you': False,
                                 'muted': False,
                                 'blocked': False
                             }),
                            ('test_user1', 'test_user3', {
                                 'following': True,
                                 'follows_you': True,
                                 'muted': True,
                                 'blocked': False
                             }),
                            ('test_user2', 'test_user3', {
                                 'following': True,
                                 'follows_you': False,
                                 'muted': False,
                                 'blocked': False
                             }),
                            ('test_user2', 'test_user1', {
                                 'following': False,
                                 'follows_you': False,
                                 'muted': False,
                                 'blocked': True
                             }),
                            ('test_user3', 'test_user1', {
                                 'following': True,
                                 'follows_you': True,
                                 'muted': False,
                                 'blocked': False
                             }),
                            ('test_user3', 'test_user2', {
                                 'following': False,
                                 'follows_you': True,
                                 'muted': False,
                                 'blocked': False
                             }),
                            ('test_user3', 'test_user3', {
                                 'following': None,
                                 'follows_you': None,
                                 'muted': None,
                                 'blocked': None
                             })
                         ])
def test_get_friendship(authorized_username, required_username, expected_output):
    friendship = actions.get_friendship(authorized_username, required_username)
    assert friendship == expected_output


@pytest.mark.parametrize("authorized_username, required_username, expected_output",
                         [
                             ('test_user1', 'test_user2', User({
                                 'username': 'test_user2',
                                 'screen_name': 'test2',
                                 'profile_image_url': 'profile.jpg',
                                 'following': False,
                                 'follows_you': False,
                                 'muted': False,
                                 'blocked': False
                             }))
                         ])
def test_get_user(authorized_username, required_username, expected_output):
    user = actions.get_user(authorized_username, required_username)
    assert isinstance(user, User)
    assert user.to_json() == expected_output.to_json()


def test_get_kweek_mentions():
    query = " SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1"
    kweek_id = db_manager.execute_query(query)[0]['id']
    actual_mention = actions.get_kweek_mentions(kweek_id)[0]
    expected_mention = Mention({
                                    'username': 'test_user3',
                                    'indices': [1, 2]
                               })
    assert isinstance(actual_mention, Mention)
    assert actual_mention.to_json() == expected_mention.to_json()

    query = "SELECT ID FROM KWEEK WHERE USERNAME = 'test_user2' LIMIT 1"
    kweek_id = db_manager.execute_query(query)[0]['id']
    mentions = actions.get_kweek_hashtags(kweek_id)
    assert mentions == []


def test_get_kweek_hashtags():
    query = " SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3' LIMIT 1"
    kweek_id = db_manager.execute_query(query)[0]['id']
    actual_hashtag = actions.get_kweek_hashtags(kweek_id)[0]
    query = "SELECT ID FROM HASHTAG WHERE TEXT='trend' LIMIT 1"
    hashtag_id = db_manager.execute_query(query)[0]['id']
    expected_hashtag = Hashtag({
                                    'id': hashtag_id,
                                    'indices': [1, 2],
                                    'text': 'trend'
                               })
    assert isinstance(expected_hashtag, Hashtag)
    assert actual_hashtag.to_json() == expected_hashtag.to_json()

    query = "SELECT ID FROM KWEEK WHERE USERNAME = 'test_user2' LIMIT 1"
    kweek_id = db_manager.execute_query(query)[0]['id']
    hashtags = actions.get_kweek_hashtags(kweek_id)
    assert hashtags == []


def test_get_kweek_statistics():
    query = "SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1' LIMIT 1"
    kweek_id = db_manager.execute_query(query)[0]['id']

    authorized_username = 'test_user3'
    actual_kweek_statistics = actions.get_kweek_statistics(authorized_username, kweek_id)
    expected_kweek_statistics = {
                                    'number_of_likes': 1,
                                    'number_of_rekweeks': 1,
                                    'number_of_replies': 0,
                                    'liked_by_user': True,
                                    'rekweeked_by_user': True
                                }
    assert actual_kweek_statistics == expected_kweek_statistics

    authorized_username = 'test_user2'
    actual_kweek_statistics = actions.get_kweek_statistics(authorized_username, kweek_id)
    expected_kweek_statistics = {
                                    'number_of_likes': 1,
                                    'number_of_rekweeks': 1,
                                    'number_of_replies': 0,
                                    'liked_by_user': False,
                                    'rekweeked_by_user': False
                                }
    assert actual_kweek_statistics == expected_kweek_statistics


@pytest.mark.parametrize("username, expected_output",
                         [
                             ('test_user1', True),
                             ('test_user2', True),
                             ('test_user4', False)
                         ])
def test_is_user(username, expected_output):
    assert actions.is_user(username) == expected_output


def test_paginate():
    dictionaries_list = [
        {
            'id': 1,
            'text': 'one'
        },
        {
            'id': 2,
            'text': 'two'
        },
        {
            'id': 3,
            'text': 'three'
        },
        {
            'id': 4,
            'text': 'four'
        }
    ]
    # Normal operation
    new_list = actions.paginate(dictionaries_list=dictionaries_list,
                                required_size=2, start_after_key='id', start_after_value=2)

    assert new_list == [
        {
            'id': 3,
            'text': 'three'
        },
        {
            'id': 4,
            'text': 'four'
        }
    ]
    # ID does not exist
    new_list = actions.paginate(dictionaries_list=dictionaries_list,
                                required_size=2, start_after_key='id', start_after_value=5)

    assert new_list is None
    # Start after value is None
    new_list = actions.paginate(dictionaries_list=dictionaries_list,
                                required_size=2, start_after_key='id', start_after_value=None)

    assert new_list == [{
            'id': 1,
            'text': 'one'
        },
        {
            'id': 2,
            'text': 'two'
        }]
    # Invalid key
    exception_caught = False
    try:
        actions.paginate(dictionaries_list=dictionaries_list,
                         required_size=2, start_after_key='no_id',
                         start_after_value=5)
    except TypeError as E:
        exception_caught = True
        assert str(E) == 'One or more dictionary in dictionaries_list do not contain the provided key.'

    assert exception_caught
    # Invalid list
    exception_caught = False
    try:
        actions.paginate(dictionaries_list=None,
                         required_size=2, start_after_key='id',
                         start_after_value=5)
    except TypeError as E:
        exception_caught = True
        assert str(E) == 'dictionaries_list parameter passed was not a list.'

    assert exception_caught
    # Invalid list items
    exception_caught = False
    try:
        actions.paginate(dictionaries_list=[1, 2, 3],
                         required_size=2, start_after_key='id',
                         start_after_value=5)
    except TypeError as E:
        exception_caught = True
        assert str(E) == 'One or more values in dictionaries_list are not a dictionary.'

    assert exception_caught


def test_get_profile_kweeks():
    expected_kweeks = []

    query = """
                       SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1'
                       AND TEXT = 'Test user 1, third kweek'
                   """
    kweek_id = db_manager.execute_query(query)[0]['id']
    expected_kweeks.append(Kweek({
        'id': kweek_id,
        'created_at': datetime.strptime('2016-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        'text': 'Test user 1, third kweek',
        'media_url': None,
        'user': actions.get_user('test_user2', 'test_user1'),
        'mentions': actions.get_kweek_mentions(kweek_id),
        'hashtags': actions.get_kweek_hashtags(kweek_id),
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    }))

    query = """
                    SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1'
                    AND TEXT = 'Test user 1, second kweek'
                """
    kweek_id = db_manager.execute_query(query)[0]['id']
    expected_kweeks.append(Kweek({
        'id': kweek_id,
        'created_at': datetime.strptime('2013-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        'text': 'Test user 1, second kweek',
        'media_url': None,
        'user': actions.get_user('test_user2', 'test_user1'),
        'mentions': actions.get_kweek_mentions(kweek_id),
        'hashtags': actions.get_kweek_hashtags(kweek_id),
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    }))

    query = """
                    SELECT ID FROM KWEEK WHERE USERNAME = 'test_user3'
                    AND TEXT = 'Test user 3, first kweek'
                """
    kweek_id = db_manager.execute_query(query)[0]['id']
    expected_kweeks.append(Kweek({
        'id': kweek_id,
        'created_at': datetime.strptime('2012-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        'text': 'Test user 3, first kweek',
        'media_url': None,
        'user': actions.get_user('test_user2', 'test_user3'),
        'mentions': actions.get_kweek_mentions(kweek_id),
        'hashtags': actions.get_kweek_hashtags(kweek_id),
        'number_of_likes': 0,
        'number_of_rekweeks': 1,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': RekweekInfo({
            'rekweeker_name': 'test1',
            'rekweeker_username': 'test_user1'
        }),
        'liked_by_user': False,
        'rekweeked_by_user': False
    }))

    query = """
                    SELECT ID FROM KWEEK WHERE USERNAME = 'test_user1'
                    AND TEXT = 'Test user 1, first kweek'
                """
    kweek_id = db_manager.execute_query(query)[0]['id']
    expected_kweeks.append(Kweek({
        'id': kweek_id,
        'created_at': datetime.strptime('2010-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        'text': 'Test user 1, first kweek',
        'media_url': None,
        'user': actions.get_user('test_user2', 'test_user1'),
        'mentions': actions.get_kweek_mentions(kweek_id),
        'hashtags': actions.get_kweek_hashtags(kweek_id),
        'number_of_likes': 1,
        'number_of_rekweeks': 1,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    }))

    # Normal case
    actual_kweeks = actions.get_profile_kweeks('test_user2', 'test_user1', None)

    for index, kweek in enumerate(actual_kweeks):
        assert expected_kweeks[index].to_json() == kweek.to_json()

    # Invalid ID
    exception_caught = False
    try:
        actions.get_profile_kweeks('test_user2', 'test_user1', 'invalid_id')
    except ValueError:
        exception_caught = True
    assert exception_caught
