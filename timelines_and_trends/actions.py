from . import query_factory
from models import User, Mention, Hashtag, Kweek


def get_friendship(authorized_username, required_username):
    friendship = query_factory.get_friendship(authorized_username=authorized_username,
                                              required_username=required_username)
    return friendship


def get_user(authorized_username, required_username):
    user = query_factory.get_user_data(required_username)
    friendship = query_factory.get_friendship(authorized_username=authorized_username,
                                              required_username=required_username)
    user.update(friendship)
    return User(user)


def get_kweek_mentions(kweek_id):
    database_mentions = query_factory.get_kweek_mentions(kweek_id)
    mentions = []
    for database_mention in database_mentions:
        mention = {
            'username': database_mention['username'],
            'indices': [database_mention['starting_index'], database_mention['ending_index']]
        }
        mentions.append(Mention(mention))
    return mentions


def get_kweek_hashtags(kweek_id):
    database_hashtags = query_factory.get_kweek_hashtags(kweek_id)
    hashtags = []
    for database_hashtag in database_hashtags:
        hashtag = {
            'id': database_hashtag['hashtag_id'],
            'indices': [database_hashtag['starting_index'], database_hashtag['ending_index']]
        }
        hashtags.append(Hashtag(hashtag))
    return hashtags


def get_profile_kweeks(authorized_username, required_username):
    # Get a list of kweeks with missing data
    profile_kweeks = query_factory.get_profile_kweeks(required_username)
    # The profile user as a user object, will be used for most of the kweeks
    profile_user = get_user(authorized_username=authorized_username,
                            required_username=required_username)
    kweeks = []
    for kweek in profile_kweeks:
        # Add the user
        if kweek['username'] == required_username:
            kweek['user'] = profile_user
        else:
            kweek['user'] = get_user(authorized_username=authorized_username,
                                     required_username=kweek['username'])
        # Add the statistics
        kweek_statistics = get_kweek_statistics(authorized_username=authorized_username,
                                                kweek_id=kweek['id'])
        kweek.update(kweek_statistics)
        # Add mentions and hashtags
        kweek['mentions'] = get_kweek_mentions(kweek['id'])
        kweek['hashtags'] = get_kweek_hashtags(kweek['id'])
        # Add rekweek info
        if kweek['is_rekweek']:
            rekweek_info = {
                'rekweeker_name': profile_user.screen_name,
                'rekweeker_username': profile_user.username
            }
            kweek['rekweek_info'] = rekweek_info
        else:
            kweek['rekweek_info'] = None
        kweeks.append(Kweek(kweek))

    return kweeks


def is_user(username):
    return query_factory.is_user(username)


def get_kweek_statistics(authorized_username, kweek_id):
    return query_factory.get_kweek_statistics(authorized_username=authorized_username,
                                              kweek_id=kweek_id)
