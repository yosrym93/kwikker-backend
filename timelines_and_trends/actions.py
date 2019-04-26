from . import query_factory
from models import User, Mention, Hashtag, Kweek, RekweekInfo, Trend


def get_friendship(authorized_username, required_username):
    """
        Gets the friendship status of the authorized user and a different user.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *required_username (string)*: The username of the user whose friendship status is required.

        *Returns:*
            - *Dictionary*: {
                                | *following (bool)*: Is the authorized user following the required user.,
                                | *follows_you (bool)*: Is the required user following the authorized user.,
                                | *blocked (bool)*: Is the required user blocked by the authorized user.,
                                | *muted (bool)*: Is the required user muted by the authorized user.
                                | }

            Note: All the dictionary values are None if the authorized user is the same as the required user.
    """
    friendship = {}

    # The friendship checks are invalid if the authorized username is the same as the required username
    if authorized_username == required_username:
        friendship['following'] = None
        friendship['follows_you'] = None
        friendship['blocked'] = None
        friendship['muted'] = None
        return friendship

    friendship['following'] = query_factory.check_following(authorized_username, required_username)
    friendship['follows_you'] = query_factory.check_follows_you(authorized_username, required_username)
    friendship['blocked'] = query_factory.check_blocked(authorized_username, required_username)
    friendship['muted'] = query_factory.check_muted(authorized_username, required_username)

    return friendship


def get_user(authorized_username, required_username):
    """
        Constructs a user object given its username.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *required_username (string)*: The username of the user whose user object is required.

        *Returns:*
            - *models.User object*
    """
    # The query return a list containing one dictionary, the required_username is already verified to exist.
    user = query_factory.get_user_data(required_username)[0]
    friendship = get_friendship(authorized_username=authorized_username,
                                required_username=required_username)
    user.update(friendship)
    return User(user)


def get_kweek_mentions(kweek_id):
    """
        Gets the mentions in a given kweek.


        *Parameters:*
            - *kweek_id (int)*: The id of the kweek.

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
            - *kweek_id (int)*: The id of the kweek.

        *Returns:*
            - *List of models.Hashtag objects*
    """
    database_hashtags = query_factory.get_kweek_hashtags(kweek_id)
    hashtags = []
    for database_hashtag in database_hashtags:
        hashtag = {
            'id': database_hashtag['hashtag_id'],
            'indices': [database_hashtag['starting_index'], database_hashtag['ending_index']],
            'text': database_hashtag['text']
        }
        hashtags.append(Hashtag(hashtag))
    return hashtags


def get_all_trends(last_retrieved_trend_id):
    """
        Gets all the hashtags.


        *Parameters:*
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved trend (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Hashtag objects*
    """
    if last_retrieved_trend_id is not None:
        try:
            last_retrieved_trend_id = int(last_retrieved_trend_id)
        except ValueError:
            raise
    database_trends = query_factory.get_all_trends()
    # Paginate the results
    try:
        database_trends = paginate(dictionaries_list=database_trends, required_size=20,
                                   start_after_key='id', start_after_value=last_retrieved_trend_id)
    except TypeError as E:
        print(E)
        raise
    if database_trends is None:
        return None
    trends = []
    for database_trend in database_trends:
        trend = {
            'id': database_trend['id'],
            'text': database_trend['text'],
            'number_of_kweeks': database_trend['number_of_kweeks']
        }
        trends.append(Trend(trend))
    return trends


def is_trend(trend_id):
    """
        Checks if a trend id belongs to an existing trend.


        *Parameters:*
            - *trend_id (string)*: The trend id to be checked.

        *Returns:*
            - *True*: The trend id belongs to an existing trend.
            - *False*: The trend id does not exist.
    """
    try:
        trend_id = int(trend_id)
    except ValueError:
        raise
    # Check if the trend exists
    return query_factory.is_trend(trend_id)


def is_user(username):
    """
        Checks if a username belongs to an existing user.


        *Parameters:*
            - *username (string)*: The username to be checked.

        *Returns:*
            - *True*: The username belongs to an existing user.
            - *False*: The username does not exist.
    """
    return query_factory.is_user(username)


def get_kweek_statistics(authorized_username, kweek_id):
    """
        Gets the statistics of a kweek and the interactions of the authorized user with it.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *kweek_id (int)*: The id of the kweek.

        *Returns:*
            - *Dictionary*: {
                                | *number_of_likes (int)*: The number of likes of the kweek.,
                                | *number_of_rekweeks (int)*: The number of rekweeks of the kweek.,
                                | *number_of_replies (int)*: The number of replies of the kweek.,
                                | *liked_by_user (bool)*: Whether the kweek is liked by the authorized user.,
                                | *rekweeked_by_user (bool)*: Whether the kweek is rekweeked by the authorized user.
                                | }
    """
    return query_factory.get_kweek_statistics(authorized_username=authorized_username,
                                              kweek_id=kweek_id)


def paginate(dictionaries_list, required_size, start_after_key, start_after_value):
    """
        Slices a list of dictionaries, starting at a given element and producing a new list
        with the required size. Should be called inside a try block, may raise TypeError.


        *Parameters:*
            - *dictionaries_list*: The list of dictionaries to be sliced.
            - *required_size (int)*: The size of the required list.
            - *start_after_key (int)*: The dictionary key to be checked for `start_after_value`.
            - *start_after_value (int)*: The value that the new list will start after.


        *Returns:*
            - *List of Dictionaries*: A new list starting at the required element with the required size (or less).
            - | *Raises TypeError*: If the passed dictionaries_list is
              | not actually a list of dictionaries, or a dictionary does not contain a key that matches the given key.
            - None: If the element to start at does not exist.
    """

    if not isinstance(dictionaries_list, list):
        raise TypeError('dictionaries_list parameter passed was not a list.')

    if start_after_value is None:
        return dictionaries_list[: required_size]

    start_after_index = None
    for index, value in enumerate(dictionaries_list):
        if not isinstance(value, dict):
            raise TypeError('One or more values in dictionaries_list are not a dictionary.')
        if start_after_key not in value:
            raise TypeError('One or more dictionary in dictionaries_list do not contain the provided key.')
        if start_after_index is None and value[start_after_key] == start_after_value:
            start_after_index = index

    if start_after_index is None:
        return None

    return dictionaries_list[start_after_index + 1: start_after_index + 1 + required_size]


def get_replies_and_mentions_unseen_count(authorized_username):
    """
    Gets the count of the unseen replies and mentions of the authorized user.

    *Parameters:*
        -*authorized_username (string)*: The username of the authorized user.

    *Returns:*
        -*count (int)*: The number of unseen replies and mentions of the authorized user.
    """

    return query_factory.get_replies_and_mentions_unseen_count(authorized_username)


def set_replies_and_mentions_as_seen(authorized_username):
    """
        Sets the count of the unseen replies and mentions of the authorized user as seen.

        *Parameters:*
            -*authorized_username (string)*: The username of the authorized user.
    """
    return query_factory.set_replies_and_mentions_as_seen(authorized_username)


def get_kweeks(authorized_username, last_retrieved_kweek_id, db_kweeks_fetcher, args=None):
    """
        Gets kweeks fetched by a function and builds them into models.Kweek objects.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.
            - *db_kweeks_fetcher (function)*: A function that fetches kweek dictionaries from the database.
            - *args*: Positional arguments passed to db_kweeks_fetcher

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    if last_retrieved_kweek_id is not None:
        try:
            last_retrieved_kweek_id = int(last_retrieved_kweek_id)
        except ValueError:
            raise
    # Get a list of kweeks with missing data
    db_kweeks = db_kweeks_fetcher(*args)
    # Paginate the results
    try:
        db_kweeks = paginate(dictionaries_list=db_kweeks, required_size=20,
                             start_after_key='id', start_after_value=last_retrieved_kweek_id)
    except TypeError as E:
        print(E)
        raise
    if db_kweeks is None:
        return None
    return kweeks_builder(db_kweeks, authorized_username)


def kweeks_builder(db_kweeks, authorized_username):
    """
        Builds model.Kweek objects from database kweeks dictionaries.


        *Parameters:*
            - *db_kweeks (list of dictionaries)*: The kweeks fetched from the database.
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Kweek objects*
        """
    kweeks = []
    for kweek in db_kweeks:
        # Add the user
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
        if 'is_rekweek' in kweek and kweek['is_rekweek']:
            rekweeker_username = kweek['rekweeker']
            rekweeker_name = query_factory.get_user_data(required_username=rekweeker_username)[0].get('screen_name')
            rekweek_info = RekweekInfo({
                'rekweeker_name': rekweeker_name,
                'rekweeker_username': rekweeker_username
            })
            kweek['rekweek_info'] = rekweek_info
        else:
            kweek['rekweek_info'] = None
        kweeks.append(Kweek(kweek))

    return kweeks


def get_home_kweeks(authorized_username, last_retrieved_kweek_id):
    """
        Gets the kweeks that should appear on the authorized user's home timeline.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_home_kweeks,
                      args=[authorized_username])


def get_profile_kweeks(authorized_username, required_username, last_retrieved_kweek_id):
    """
        Gets the kweeks that should appear on a specific user profile.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *required_username (string)*: The username of the user whose profile kweeks are required.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_profile_kweeks,
                      args=[required_username])


def get_replies_and_mentions_timeline_kweeks(authorized_username, last_retrieved_kweek_id):
    """
        Gets the kweeks that should appear on the authorized user's replies and mentions timeline.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_replies_and_mentions_kweeks,
                      args=[authorized_username])


def get_user_liked_kweeks(authorized_username, required_username, last_retrieved_kweek_id):
    """
        Gets the kweeks that are liked by a user.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *required_username (string)*: The username of the user whose liked kweeks are required.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_user_liked_kweeks,
                      args=[required_username])


def get_trend_kweeks(authorized_username, trend_id, last_retrieved_kweek_id):
    """
        Gets the kweeks that belong to a trend.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.
            - *trend_id (string)*: The id of the trend whose kweeks are to be fetched.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_trend_kweeks,
                      args=[trend_id])


def get_search_kweeks(authorized_username, search_text, last_retrieved_kweek_id):
    """
        Gets the kweeks that correspond to the search text, ordered by relevance.


        *Parameters:*
            - *authorized_username (string)*: The username of the authorized user.
            - *last_retrieved_kweek_id (string)*: The id of the last retrieved kweek (used to fetch more). Nullable.
            - *search_text (string)*: The text entered by the user in the search bar.

        *Returns:*
            - *List of models.Kweek objects*
            - *None*: if last_retrieved_kweek_id does not exist.
            - *Raise ValueError*: if last_retrieved_kweek_id is not a valid number.
            - *Raise TypeError*: if raised by paginate.
    """
    return get_kweeks(authorized_username=authorized_username,
                      last_retrieved_kweek_id=last_retrieved_kweek_id,
                      db_kweeks_fetcher=query_factory.get_search_kweeks,
                      args=[search_text])


def check_blocked(blocker_username, blocked_username):
    return query_factory.check_blocked(blocker_username, blocked_username)
