import pytest
from . import actions
from database_manager import db_manager
from models import User, Mention, Hashtag, Kweek, RekweekInfo
from datetime import datetime

db_manager.initialize_connection('kwikker', 'postgres', '')


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
                'username': 'test_user1',
                'indices': [10, 16]}),
            Mention({
                'username': 'test_user2',
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
    print("kweek id", kid)
    query: str = """SELECT ID FROM HASHTAG ORDER BY ID DESC LIMIT 1 """
    hid = db_manager.execute_query(query)[0]['id']
    print("hahstag id ", hid)
    query: str = """SELECT ID,TEXT,media_url,username,reply_to FROM KWEEK WHERE ID= %s """
    data = (kid,)
    resulted_kweek = db_manager.execute_query(query, data)[0]
    print("kweek", resulted_kweek)
    query: str = """SELECT * FROM MENTION WHERE  KWEEK_ID= %s"""
    data = (kid,)
    resulted_mention = db_manager.execute_query(query, data)[0]
    query: str = """SELECT TEXT, KWEEK_ID, HASHTAG_ID, STARTING_INDEX, ENDING_INDEX 
     FROM KWEEK_HASHTAG JOIN HASHTAG  ON ID = HASHTAG_ID WHERE KWEEK_ID  = %s"""
    data = (kid,)
    resulted_hashtag = db_manager.execute_query(query, data)[0]
    print("hashtag", resulted_hashtag)
    expected_mention = {'kweek_id': kid, 'username': 'test_user1', 'starting_index': 10,
                        'ending_index': 16}
    expected_hahstag = {'text': '#sky', 'kweek_id': kid, 'hashtag_id': hid,
                        'starting_index': 10, 'ending_index': 16}
    expected_kweek = {'id': kid, 'text': '#testtest',
                      'media_url': None, 'username': 'test_user1', 'reply_to': None}
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
    assert message == 'Repeated mention in the same kweek'
    check, message = actions.insert_kweek(kweek_test_4)
    assert message == 'the user mentioned does not exist in the database'




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
    # first test -  first kweek#

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test1', None, 'hagar', None)
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

    actions.delete_kweek(kid1, 'hagar')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid1,)
    response = db_manager.execute_query(query, data)
    assert response == []
    # second test - first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test2', None, 'hagar', None)
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
    data = ('01-01-2010', 'test2', None, 'hagar', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag2',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag2',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    # second test- third kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test2', None, 'hagar', None)
    db_manager.execute_query_no_return(query, data)
    kid3 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag2',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag2',)
    hid3 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid3, hid3, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    actions.delete_kweek(kid1, 'hagar')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid1,)
    response = db_manager.execute_query(query, data)
    assert response == []

    query: str = """SELECT TEXT FROM HASHTAG  WHERE TEXT= %s"""
    data = ('hashtag2',)
    response = db_manager.execute_query(query, data)
    assert response != []

    # third test - first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test3', None, 'hagar', None)
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

    # third test- second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test3', None, 'hagar', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag3',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag3',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    actions.delete_kweek(kid1, 'hagar')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid1,)
    response = db_manager.execute_query(query, data)
    assert response == []

    query: str = """SELECT TEXT FROM HASHTAG  WHERE TEXT= %s"""
    data = ('hashtag3',)
    response = db_manager.execute_query(query, data)
    assert response == []

    # fourth test- first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test4', None, 'hagar', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag4',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag4',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    # fourth test- second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test4', None, 'test_user1', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag4',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag4',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    actions.delete_kweek(kid2, 'hagar')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid2,)
    response = db_manager.execute_query(query, data)
    assert response == []

    # fifth test- first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test5', None, 'hagar', None)
    db_manager.execute_query_no_return(query, data)
    kid1 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag5',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag5',)
    hid1 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid1, hid1, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    # fifth test- second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test5', None, 'test_user1', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag5',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag5',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    actions.delete_kweek(kid2, 'test_user2')

    query: str = """SELECT * FROM KWEEK WHERE  ID= %s"""
    data = (kid2,)
    response = db_manager.execute_query(query, data)
    assert response != []


#                   test get kweek              #


def test_get_kweek():
    # first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test1', None, 'test_user1', None)
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
    data = (kid1, 'test_user2', 10, 15)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO REKWEEK VALUES(%s,%s,%s) """
    data = ('test_user2', kid1, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('test_user2', kid1, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    # second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test2', None, 'test_user3', kid1)
    db_manager.execute_query_no_return(query, data)
    kid2 = str(db_manager.execute_query("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id'])

    query: str = """INSERT INTO HASHTAG(TEXT) VALUES (%s) """
    data = ('hashtag2-',)
    db_manager.execute_query_no_return(query, data)

    query: str = """SELECT ID FROM HASHTAG WHERE TEXT = %s """
    data = ('hashtag2-',)
    hid2 = db_manager.execute_query(query, data)[0]['id']

    query: str = """INSERT INTO KWEEK_HASHTAG VALUES (%s,%s,%s,%s)"""
    data = (kid2, hid2, 0, 9,)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('test_user1', kid2, '01-01-2010')

    # third kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test3', None, 'test_user1', kid1)
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
    data = ('test_user3', kid3, '01-01-2010')

    # first output #

    kweek_test1 = Kweek({
        'id': int(kid1),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test1',
        'media_url': None,
        'user': User({
            'username': 'test_user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': True,
            'follows_you': True,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'test_user2',
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
        'liked_by_user': False,
        'rekweeked_by_user': False
    })

    check_replies, message, k, r = actions.get_kweek(kid1, 'test_user3')
    print('kwweeek')
    print(k)
    print('replies')
    print(r)
    assert check_replies == True
    assert message == 'success'
    assert k.to_json() == kweek_test1.to_json()
    assert [{'id': int(kid2)}, {'id': int(kid3)}] == r


def test_get_kweek_with_replies():
    # first kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test1', None, 'test_user1', None)
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
    data = (kid1, 'test_user2', 10, 15)
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO REKWEEK VALUES(%s,%s,%s) """
    data = ('test_user2', kid1, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    query: str = """INSERT INTO FAVORITE VALUES(%s,%s,%s) """
    data = ('test_user2', kid1, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    # second kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test2', None, 'test_user2', kid1)
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
    data = ('test_user1', kid2, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    # third kweek #

    query: str = """INSERT INTO  KWEEK (CREATED_AT,TEXT,MEDIA_URL,USERNAME,REPLY_TO) VALUES(%s, %s, %s, %s,%s) """
    data = ('01-01-2010', 'test3', None, 'test_user3', kid1)
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
    data = ('test_user3', kid3, '01-01-2010')
    db_manager.execute_query_no_return(query, data)

    kweek_test1 = Kweek({
        'id': int(kid1),
        'created_at': datetime(2010, 1, 1, 0, 0),
        'text': 'test1',
        'media_url': None,
        'user': User({
            'username': 'test_user1',
            'screen_name': 'test1',
            'profile_image_url': 'image_url',
            'following': True,
            'follows_you': True,
            'muted': False,
            'blocked': False
        }),
        'mentions': [
            Mention({
                'username': 'test_user2',
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
    replies_test1 = [
        Kweek({
            'id': int(kid2),
            'created_at': datetime(2010, 1, 1, 0, 0),
            'text': 'test2',
            'media_url': None,
            'user': User({
                'username': 'test_user2',
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
                'username': 'test_user3',
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
        }),

    ]
    check_replies, message, k, r = actions.get_kweek_with_replies(kid1, 'test_user3')
    print('kwweeek')
    print(k)
    print('replies')
    print(r)
    assert True == check_replies
    assert message == 'success'
    assert k.to_json() == kweek_test1.to_json()
    for n, i in enumerate(r):
        assert i.to_json() == replies_test1[n].to_json()
