from . import query_factory
from models import User, Mention, Hashtag, Kweek


def get_friendship(authorized_username, required_username):
    """
        Gets the friendship status of the authorized user and a different user.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the user whose friendship status is required.

        *Returns:*
            - *Dictionary*: {
                                | *following*: bool,
                                | *follows_you*: bool,
                                | *muted*: bool,
                                | *blocked*: bool
                                | }

            Note: All the dictionary values are None if the authorized user is the same as the required user.
    """
    friendship = query_factory.get_friendship(authorized_username=authorized_username,
                                              required_username=required_username)
    return friendship


def get_user(authorized_username, required_username):
    """
        Constructs a user object given its username.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the user whose user object is required.

        *Returns:*
            - *models.User object*
    """
    user = query_factory.get_user_data(required_username)
    friendship = query_factory.get_friendship(authorized_username=authorized_username,
                                              required_username=required_username)
    user.update(friendship)
    return User(user)


def get_kweek_mentions(kweek_id):
    """
        Gets the mentions in a given kweek.


        *Parameters:*
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *List of models.Mention objects*
    """
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
    """
        Gets the hashtags in a given kweek.


        *Parameters:*
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *List of models.Hashtag objects*
    """
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
    """
        Gets the kweeks that should appear on a specific user profile.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *required_username*: The username of the user whose user object is required.

        *Returns:*
            - *List of models.Kweek objects*
    """
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
        print(kweek)
        kweeks.append(Kweek(kweek))

    return kweeks


def is_user(username):
    """
        Checks if a username belongs to an existing user.


        *Parameters:*
            - *username*: The username to be checked.

        *Returns:*
            *True*: The username belongs to an existing user.
            *False*: The username does not exist.
    """
    return query_factory.is_user(username)


def get_kweek_statistics(authorized_username, kweek_id):
    """
        Gets the statistics of a kweek and the interactions of the authorized user with it.


        *Parameters:*
            - *authorized_username*: The username of the authorized user.
            - *kweek_id*: The id of the kweek.

        *Returns:*
            - *Dictionary*: {
                                | *number_of_likes*: int,
                                | *number_of_rekweeks*: int,
                                | *number_of_replies*: int,
                                | *liked_by_user*: bool,
                                | *rekweeked_by_user*: bool
                                | }
    """
    return query_factory.get_kweek_statistics(authorized_username=authorized_username,
                                              kweek_id=kweek_id)


def paginate(dictionaries_list, required_size, start_after_key, start_after_value):
    """
        Slices a list of dictionaries, starting at a given element and producing a new list
        with the required size.


        *Parameters:*
            - *dictionaries_list*: The list of dictionaries to be sliced.
            - *required_size*: The size of the required list.
            - *start_after_key*: The dictionary key to be checked for `start_after_value`.
            - *start_after_value*: The value that the new list will start after.


        *Returns:*
            - *List of Dictionaries*: A new list starting at the required element with the required size (or less).
            - | *None*: If the element to start at does not exist, the passed dictionaries_list is
              | not actually a list of dictionaries, or a dictionary does not contain a key that matches the given key.
    """
    if not isinstance(dictionaries_list, list):
        return None

    start_after_index = None
    for index, value in enumerate(dictionaries_list):
        if not isinstance(value, dict):
            return None
        if start_after_key not in value:
            return None
        if start_after_index is None and value[start_after_key] == start_after_value:
            start_after_index = index

    if start_after_index is None:
        return None

    return dictionaries_list[start_after_index + 1: start_after_index + 1 + required_size]

