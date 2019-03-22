import pytest
from . import actions
from database_manager import db_manager
from models import User, Mention, Hashtag, Kweek
from datetime import datetime

db_manager.initialize_connection('kwikker', 'postgres', '8949649')


def test_insert_kweek():
    kweek_test = Kweek({
                                 'id': 0,
                                 'created_at': datetime.utcnow(),
                                 'text': '#testtest',
                                 'media_url': None,
                                 'user': User({
                                     'username': 'test_user1',
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
                                         'indices': [18, 20]},
                                     )
                                 ],
                                 'hashtags': [
                                     Hashtag({
                                         'text': '#int',
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
                                 'text': '#testtest',
                                 'media_url': None,
                                 'user': User({
                                     'username': 'test_user1',
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
                                         'text': '#int',
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
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    first_count = db_manager.execute_query(query)[0]['count']
    actions.insert_kweek(kweek_test)
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
    expected_mention = {'kweek_id': kid, 'username': 'test_user1', 'starting_index': 10,
                        'ending_index': 16}
    expected_hahstag = {'text': '#int', 'kweek_id': kid, 'hashtag_id': hid,
                        'starting_index': 10, 'ending_index': 16}
    expected_kweek = {'id': kid, 'text': '#testtest',
                      'media_url': None, 'username': 'test_user1', 'reply_to': None}
    assert expected_kweek == resulted_kweek
    assert expected_hahstag == resulted_hashtag
    assert expected_mention == resulted_mention
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    second_count = db_manager.execute_query(query)[0]['count']
    assert (second_count - first_count) == 1
    actions.insert_kweek(kweek_test_2)
    query: str = """SELECT COUNT(*) FROM HASHTAG """
    third_count = db_manager.execute_query(query)[0]['count']
    assert third_count - second_count == 0


@pytest.mark.parametrize("authorized_username,request_kweek, expected_output",
                         [
                             ('false_username', {
                                 'text': "#first tweet",
                                 'reply_to': None,
                             }, (False, 'The authorized user does not exist in the data base')),
                             ('test_user1', {
                                 'text': "#first tweet",
                                 'reply_to': None
                             }, (True, 'success')),
                             ('test_user1', {
                                 'text': "#first tweet",
                                 'reply_to': 0
                             }, (False, 'Kweek does not exist ')),
                             ('test_user1', {
                                 'text': "#first tweet",
                                 'reply_to': db_manager.execute_query
                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']
                             }, (True, 'success')),
                             ('test_user1', {
                                 'text': "",
                                 'reply_to': db_manager.execute_query
                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']
                             }, (False, 'No text body found')),
                             ('test_user1', {
                                 'text': "  ",
                                 'reply_to': db_manager.execute_query
                                 ("""SELECT ID FROM KWEEK ORDER BY ID DESC LIMIT 1 """)[0]['id']
                             }, (False, 'No text body found'))



                         ])
def test_create_kweek(authorized_username, request_kweek, expected_output):
    check, message = actions.create_kweek(request_kweek, authorized_username)
    assert (check, message) == expected_output
