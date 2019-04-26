import pytest
from . import actions
from database_manager import db_manager
from models import User, Mention, Hashtag, Kweek
from datetime import datetime


def test_insert_kweek():
    kweek_test_1 = Kweek({
        'id': 0,
        'created_at': datetime.utcnow(),
        'text': '#test1',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': False,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user1',
                'indices': [10, 16]}),
            Mention({
                'username': 'user2',
                'indices': [18, 20]},
            )
        ],
        'hashtags': [
            Hashtag({
                'text': '#sky',
                'indices': [10, 16],
                'id': 0
            })
        ],
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })
    kweek_test_2 = Kweek({
        'id': 0,
        'created_at': datetime.utcnow(),
        'text': '#test2',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': False,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user1',
                'indices': [10, 16]}),
            Mention({
                'username': 'user2',
                'indices': [18, 20]})
        ],
        'hashtags': [
            Hashtag({
                'text': '#sky',
                'indices': [10, 16],
                'id': 0
            })
        ],
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })
    kweek_test_3 = Kweek({
        'id': 0,
        'created_at': datetime.utcnow(),
        'text': '#test3',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': False,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user1',
                'indices': [10, 16]}),
            Mention({
                'username': 'user1',
                'indices': [18, 20]},
            )
        ],
        'hashtags': [
            Hashtag({
                'text': '#sky',
                'indices': [10, 16],
                'id': 0
            })
        ],
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })
    kweek_test_4 = Kweek({
        'id': 0,
        'created_at': datetime.utcnow(),
        'text': '#test1',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': False,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user1',
                'indices': [10, 16]}),
            Mention({
                'username': 'user5',
                'indices': [18, 20]},
            )
        ],
        'hashtags': [
            Hashtag({
                'text': '#sky',
                'indices': [10, 16],
                'id': 0
            })
        ],
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })
    query: str = """SELECT ID FROM HASHTAG WHERE TEXT=%s  """
    data = ('#sky',)
    hid = db_manager.execute_query(query, data)
    if len(hid) != 0:
        query: str = """DELETE FROM HASHTAG WHERE ID=%s  """
        data = (hid[0]['id'],)
        db_manager.execute_query_no_return(query, data)
        query: str = """DELETE FROM KWEEK_HASHTAG WHERE HASHTAG_ID=%s  """
        data = (hid[0]['id'],)
        db_manager.execute_query_no_return(query, data)
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    first_count = db_manager.execute_query(query)[0]['count']
    actions.insert_kweek(kweek_test_1)
    query: str = """SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """
    kid = db_manager.execute_query(query)[0]['id']
    query: str = """SELECT ID FROM HASHTAG ORDER BY ID DESC LIMIT 1 """
    hid = db_manager.execute_query(query)[0]['id']
    query: str = """SELECT ID,TEXT,media_url,username,reply_to FROM KWEEK WHERE ID= %s """
    data = (kid,)
    resulted_kweek = db_manager.execute_query(query, data)[0]
    query: str = """SELECT * FROM MENTION WHERE  KWEEK_ID= %s"""
    data = (kid,)
    resulted_mention = db_manager.execute_query(query, data)[0]
    query: str = """SELECT TEXT, KWEEK_ID, HASHTAG_ID, STARTING_INDEX, ENDING_INDEX 
     FROM KWEEK_HASHTAG JOIN HASHTAG  ON ID = HASHTAG_ID WHERE KWEEK_ID  = %s"""
    data = (kid,)
    resulted_hashtag = db_manager.execute_query(query, data)[0]
    expected_mention = {'kweek_id': kid, 'username': 'user1', 'starting_index': 10,
                        'ending_index': 16}
    expected_hahstag = {'text': '#sky', 'kweek_id': kid, 'hashtag_id': hid,
                        'starting_index': 10, 'ending_index': 16}
    expected_kweek = {'id': kid, 'text': '#test1',
                      'media_url': None, 'username': 'user1', 'reply_to': None}
    assert expected_kweek == resulted_kweek
    assert expected_hahstag == resulted_hashtag
    assert expected_mention == resulted_mention
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    second_count = db_manager.execute_query(query)[0]['count']
    assert (second_count - first_count) == 1
    check, message = actions.insert_kweek(kweek_test_2)
    assert message == 'success'
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    third_count = db_manager.execute_query(query)[0]['count']
    assert third_count - second_count == 0
    check, message = actions.insert_kweek(kweek_test_3)
    assert message == 'success'
    check, message = actions.insert_kweek(kweek_test_4)
    assert message == 'success'


@pytest.mark.parametrize("authorized_username,request_kweek, expected_output",
                         [
                             ('false_username', {
                                 'text': "#first tweet",
                                 'reply_to': None,
                                 'media_id': None
                             }, (False, 'The authorized user does not exist in the data base')),
                             ('user1', {
                                 'text': "#first tweet",
                                 'reply_to': None,
                                  'media_id': None
                             }, (True, 'success')),
                             ('user1', {
                                 'text': "#first tweet",
                                 'reply_to': str(db_manager.execute_query
                                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']),
                                 'media_id': None

                             }, (True, 'success')),
                             ('user1', {
                                 'text': "",
                                 'reply_to': str(db_manager.execute_query
                                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']),
                                 'media_id': None
                             }, (False, 'No text body found')),
                             ('user1', {
                                 'text': "  ",
                                 'reply_to': str(db_manager.execute_query
                                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']),
                                 'media_id' : None
                             }, (False, 'No text body found')),
                             ('user1', {
                                 'text': "test",
                                 'reply_to': "ahmed",
                                 'media_id' : None
                             }, (False, 'Not valid id')),
                             ('user1', {
                                 'text': "test",
                                 'reply_to': '',
                                 'media_id': None
                             }, (False, 'No reply body found')),
                             ('user1', {
                                 'text': "#first tweet",
                                 'reply_to': ' ',
                                 'media_id': None
                             }, (False, 'No reply body found')),
                             ('user1', {
                                 'text': "#first tweet",
                                 'reply_to': '1000000000',
                                 'media_id': None
                             }, (False, 'Kweek does not exist '))


                         ])
def test_create_kweek(authorized_username, request_kweek, expected_output):
    check, message = actions.create_kweek(request_kweek, authorized_username)
    assert (check, message) == expected_output


@pytest.mark.parametrize("parameter, expected_output",
                         [
                             ('-1',
                              (False, 'Kweek is not available')),
                             (str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)
                                  [0]['id']),
                              (True, 'success')),
                             ('abc',
                              (False, 'Invalid data type'))
                         ])
def test_validate_request(parameter, expected_output):
    check, message = actions.validate_request(parameter)
    assert (check, message) == expected_output


@pytest.mark.parametrize("text, expected_hashtags, expected_mentions",
                         [
                             ('#hashtag and @mention',
                              [Hashtag({'indices': (0, 8), 'text': '#hashtag', 'id': 0})],
                              [Mention({'indices': (13, 21), 'username': 'mention'})]),
                             ('#hashtag and @mention ',
                              [Hashtag({'indices': (0, 8), 'text': '#hashtag', 'id': 0})],
                              [Mention({'indices': (13, 21), 'username': 'mention'})]),
                             ('@mention and #hashtag',
                              [Hashtag({'indices': (13, 21), 'text': '#hashtag', 'id': 0})],
                              [Mention({'indices': (0, 8), 'username': 'mention'})]),
                             ('@mention and #hashtag ',
                              [Hashtag({'indices': (13, 21), 'text': '#hashtag', 'id': 0})],
                              [Mention({'indices': (0, 8), 'username': 'mention'})]),
                             ('@mention and # ',
                              [Hashtag({'indices': (13, 14), 'text': '#', 'id': 0})],
                              [Mention({'indices': (0, 8), 'username': 'mention'})]),
                             ('@mention and #',
                              [],
                              [Mention({'indices': (0, 8), 'username': 'mention'})]),
                             ('@mention1 @mention2 and #hashtag1 and hashtag2 ',
                              [Hashtag({'indices': (24, 33), 'text': '#hashtag1', 'id': 0})],
                              [Mention({'indices': (0, 9), 'username': 'mention1'}),
                               Mention({'indices': (10, 19), 'username': 'mention2'})]),
                             ('smth',
                              [],
                              [])

                         ])
def test_extract_mentions_hashtags(text, expected_hashtags, expected_mentions):
    h, m = actions.extract_mentions_hashtags(text)
    for r, i in enumerate(h):
        assert i.to_json() == expected_hashtags[r].to_json()
    for r, i in enumerate(m):
        assert i.to_json() == expected_mentions[r].to_json()


def test_delete_kweek():
    # first test:delete normal kweek -  first kweek#

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test1', None, 'user1', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])
    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag1',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag1',)
    hid1 = db_manager.execute_query(query, data)[0]['id']
    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    check, message = actions.delete_kweek(kid1, 'user1')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid1,)
    response = db_manager.execute_query(query, data)
    assert response == []
    assert message == 'success'

    # second test: test update hashtag - first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test2', None, 'user1', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])
    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag2',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag2',)
    hid1 = db_manager.execute_query(query, data)[0]['id']
    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)
    # second test- second kweek #
    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test2', None, 'user1', None)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])
    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    actions.delete_kweek(kid1, 'user1')
    query: str = """SELECT TEXT FROM HASHTAG WHERE TEXT= %s"""
    data = ('hashtag2',)
    response = db_manager.execute_query(query, data)
    assert response != []

    actions.delete_kweek(kid2, 'user1')
    query: str = """SELECT TEXT FROM HASHTAG WHERE TEXT= %s"""
    data = ('hashtag2',)
    response = db_manager.execute_query(query, data)
    assert response == []

    # third test: user is not kweek writer

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test3', None, 'user1', 'None')
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag3',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag3',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    check, message = actions.delete_kweek(kid1, 'user2')
    assert message == 'Deletion is not allowed'

    # fourth test : user is not kweek owner

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test3', None, 'user2', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag3',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag3',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    check, message = actions.delete_kweek(kid1, 'user3')
    assert message == 'Deletion is not allowed'

    # fifth test: user is  kweek owner

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test3', None, 'user1', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)
    check, message = actions.delete_kweek(kid2, 'user2')
    assert message == 'success'

    # sixth test: kweek doesn't exist

    check, message = actions.delete_kweek('-1', 'user2')
    assert message == 'Kweek is not available'
    check, message = actions.delete_kweek('ahmed', 'user2')
    assert message == 'Invalid data type'


def test_get_kweek():
    # first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test1', None, 'user1', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag1-',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag1-',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO MENTION VALUES(%s,%s,%s,%s) """
    data = (kid1, 'user2', 10, 15)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO REKWEEK VALUES(%s,%s,%s) """
    data = ('user3', kid1, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('user3', kid1, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    # second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test2', None, 'user2', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    # third kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test3', None, 'user1', kid1)
    db_manager.execute_query_no_return(query, data)
    kid3 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag3-',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag3-',)
    hid3 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid3, hid3, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('user3', kid3, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    # first output #

    kweek_test1 = Kweek({
        'id': int(kid1),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test1',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': True,
            'follows_you': True,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user2',
                'indices': [10, 15]})

        ],
        'hashtags': [
            Hashtag({
                'text': 'hashtag1-',
                'indices': [0, 9],
                'id': hid1
            })
        ],
        'number_of_likes': 1,
        'number_of_rekweeks': 1,
        'number_of_replies': 2,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': True,
        'rekweeked_by_user': True
    })

    kweek_test2 = Kweek({
        'id': int(kid2),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test2',
        'media_url': None,
        'user': User({
            'username': 'user2',
            'screen_name': 'test2',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': False,
            'muted': False,
            'blocked': False
        }),
        'mentions': [

        ],
        'hashtags': [

        ],
        'number_of_likes': 0,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': int(kid1),
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })

    check_replies, message, k, r = actions.get_kweek(kid1, 'user3', False)
    assert message == 'success'
    assert k.to_json() == kweek_test1.to_json()
    assert [{'id': int(kid2)}, {'id': int(kid3)}] == r

    check_replies, message, k, r = actions.get_kweek(kid2, 'user1', False)
    assert message == 'success'
    assert k.to_json() == kweek_test2.to_json()
    assert [] == r

    check_replies, message, k, r = actions.get_kweek('ahmed', 'user1', False)
    assert message == 'Invalid data type'

    check_replies, message, k, r = actions.get_kweek('-1', 'user1', False)
    assert message == 'Kweek is not available'

    check_replies, message, k, r = actions.get_kweek(kid1, 'user3', True)
    assert message == 'success'
    assert k is None
    assert [{'id': int(kid2)}, {'id': int(kid3)}] == r


def test_get_kweek_with_replies():
    # first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test1', None, 'user1', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag1---',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag1---',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO MENTION VALUES(%s,%s,%s,%s) """
    data = (kid1, 'user2', 10, 15)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO REKWEEK VALUES(%s,%s,%s) """
    data = ('user2', kid1, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('user2', kid1, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    # second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test2', None, 'user2', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag2---',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag2---',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('user1', kid2, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    # third kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('2010-01-01', 'test3', None, 'user3', kid1)
    db_manager.execute_query_no_return(query, data)
    kid3 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag3---',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag3---',)
    hid3 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid3, hid3, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('user3', kid3, '2010-01-01')
    db_manager.execute_query_no_return(query, data)

    kweek_test1 = Kweek({
        'id': int(kid1),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test1',
        'media_url': None,
        'user': User({
            'username': 'user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': True,
            'follows_you': True,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'user2',
                'indices': [10, 15]})

        ],
        'hashtags': [
            Hashtag({
                'text': 'hashtag1---',
                'indices': [0, 9],
                'id': hid1
            })
        ],
        'number_of_likes': 1,
        'number_of_rekweeks': 1,
        'number_of_replies': 2,
        'reply_to': None,
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
    })
    kweek_test2 = Kweek({
        'id': int(kid2),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test2',
        'media_url': None,
        'user': User({
            'username': 'user2',
            'screen_name': 'test2',
            'profile_image_url': 'image_url',
            'following': False,
            'follows_you': True,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
        ],
        'hashtags': [
            Hashtag({
                'text': 'hashtag2---',
                'indices': [0, 9],
                'id': hid2
            })
        ],
        'number_of_likes': 1,
        'number_of_rekweeks': 0,
        'number_of_replies': 0,
        'reply_to': int(kid1),
        'rekweek_info': None,
        'liked_by_user': False,
        'rekweeked_by_user': False
        })
    replies_test1 = [
        Kweek({
            'id': int(kid2),
            'created_at': datetime(2010, 1, 1, 0, 0),
            'text': 'test2',
            'media_url': None,
            'user': User({
                'username': 'user2',
                'screen_name': 'test2',
                'profile_image_url': 'image_url',
                'following': False,
                'follows_you': True,
                'muted': False,
                'blocked': False
            }),
            'mentions': [
            ],
            'hashtags': [
                Hashtag({
                    'text': 'hashtag2---',
                    'indices': [0, 9],
                    'id': hid2
                })
            ],
            'number_of_likes': 1,
            'number_of_rekweeks': 0,
            'number_of_replies': 0,
            'reply_to': int(kid1),
            'rekweek_info': None,
            'liked_by_user': False,
            'rekweeked_by_user': False
        }), Kweek({
            'id': int(kid3),
            'created_at': datetime(2010, 1, 1, 0, 0),
            'text': 'test3',
            'media_url': None,
            'user': User({
                'username': 'user3',
                'screen_name': 'test3',
                'profile_image_url': 'image_url',
                'following': False,
                'follows_you': False,
                'muted': False,
                'blocked': False
            }),
            'mentions': [
            ],
            'hashtags': [
                Hashtag({
                    'text': 'hashtag3---',
                    'indices': [0, 9],
                    'id': hid3
                })
            ],
            'number_of_likes': 1,
            'number_of_rekweeks': 0,
            'number_of_replies': 0,
            'reply_to': int(kid1),
            'rekweek_info': None,
            'liked_by_user': True,
            'rekweeked_by_user': False
        })

    ]
    check_replies, message, k, r = actions.get_kweek_with_replies(kid1, 'user3', False)
    assert message == 'success'
    assert k.to_json() == kweek_test1.to_json()
    for n, i in enumerate(r):
        assert i.to_json() == replies_test1[n].to_json()

    check_replies, message, k, r = actions.get_kweek_with_replies('ahmed', 'user3', False)
    assert message == 'Invalid data type'
    assert r == []
    assert k is None

    check_replies, message, k, r = actions.get_kweek_with_replies(kid2, 'user3', False)
    assert message == 'success'
    assert k.to_json() == kweek_test2.to_json()
    assert r == []
