from . import query_factory
from models import UserProfile, User
from timelines_and_trends import actions as timelines_and_trends_actions
from users_profiles import actions as users_profile_actions, query_factory as users_profile_query_factory
from notifications import actions as notif_actions

size = 3
"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def get_profile_followers(username, last_retrieved_username, authorized_username):
    """
                    The function returns a list of UserProfile objects of the followers users.

                    *Parameters*:
                        - *username (string)*: The user that is logged in now.
                        - *last_retrieved_username(string)*: The last user in the previous list.

                    *Returns*:
                        - *follower_list*: a list of objects of UsersProfiles.
    """

    followers = query_factory.get_followers(username)
    try:
        followers = timelines_and_trends_actions.paginate(dictionaries_list=followers, required_size=size,
                                                          start_after_key='username',
                                                          start_after_value=last_retrieved_username)
    except TypeError as E:
        print(E)
        raise
    if followers is None:
        return None
    user_profile_list = []
    for follower in followers:
        follower["followers_count"] = users_profile_query_factory.get_user_followers(follower['username'])["count"]
        follower["following_count"] = users_profile_query_factory.get_user_following(follower['username'])["count"]
        follower["kweeks_count"] = users_profile_query_factory.get_number_of_kweeks(follower['username'])['count']
        follower["likes_count"] = users_profile_query_factory.get_number_of_likes(follower['username'])['count']
        friendship = timelines_and_trends_actions.get_friendship(authorized_username, follower['username'])
        follower.update(friendship)
        user_profile_list.append(UserProfile(follower))
    return user_profile_list


def get_profile_following(username, last_retrieved_username, authorized_username):
    """
                        The function returns a list of UserProfile objects of the followed users.

                        *Parameters*:
                            - *username (string)*: The user that is logged in now.
                            - *last_retrieved_username(string)*: The last user in the previous list.

                        *Returns*:
                            - *followed_list*: a list of objects of UsersProfiles.
    """

    followed = query_factory.get_following(username)
    try:
        followed = timelines_and_trends_actions.paginate(dictionaries_list=followed, required_size=size,
                                                         start_after_key='username',
                                                         start_after_value=last_retrieved_username)
    except TypeError as E:
        print(E)
        raise
    if followed is None:
        return None
    user_profile_list = []
    for follower in followed:
        follower["followers_count"] = users_profile_query_factory.get_user_followers(follower['username'])["count"]
        follower["following_count"] = users_profile_query_factory.get_user_following(follower['username'])["count"]
        follower["kweeks_count"] = users_profile_query_factory.get_number_of_kweeks(follower['username'])['count']
        follower["likes_count"] = users_profile_query_factory.get_number_of_likes(follower['username'])['count']
        friendship = timelines_and_trends_actions.get_friendship(authorized_username, follower['username'])
        follower.update(friendship)
        user_profile_list.append(UserProfile(follower))
    return user_profile_list


def follow(username, authorized_username):
    """
                        The function add username to the following list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be followed.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    blocked = query_factory.if_blocked(username, authorized_username)['count']
    if blocked == 1:
        return "you can not follow this user you have been blocked by him."
    blocked = query_factory.if_blocked(authorized_username, username)['count']
    if blocked == 1:
        return "you can not follow this account you have been blocked this account, to follow un block him."
    check = query_factory.check_if_follow(authorized_username, username)['count']
    if check == 1:
        return "you already following that user."
    response = query_factory.follow(authorized_username, username)
    notif_actions.create_notifications(authorized_username, username, 'FOLLOW')
    return response


def unfollow(username, authorized_username):
    """
                        The function delete username from the following list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be unfollowed.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    check = query_factory.check_if_follow(authorized_username, username)['count']
    if check == 0:
        return "you already not following that user"
    response = query_factory.unfollow(authorized_username, username)
    return response


def get_muted_users(authorized_username):
    """
                        The function gets a list of muted user.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.

                        *Returns*:
                            - *response*: a list of user objects of muted users.
    """
    muted = query_factory.get_muted_list(authorized_username)
    user_list = []
    for muted_user in muted:
        friendship = timelines_and_trends_actions.get_friendship(authorized_username, muted_user['username'])
        muted_user.update(friendship)
        user_list.append(User(muted_user))
    return user_list


def mute(authorized_username, username):
    """
                        The function add username to the muted list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be muted.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    check = query_factory.if_muted(authorized_username, username)["count"]
    if check == 1:
        return "user already muted"
    response = query_factory.mute(authorized_username, username)
    return response


def unmute(authorized_username, username):
    """
                        The function delete username from the muted list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be unmuted.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    check = query_factory.if_muted(authorized_username, username)["count"]
    if check == 0:
        return "user already unmuted"
    response = query_factory.unmute(authorized_username, username)
    return response


def get_blocked_users(authorized_username):
    """
                        The function gets a list of blocked user.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.

                        *Returns*:
                            - *response*: a list of user objects of blocked users.
    """
    blocked = query_factory.get_blocked_list(authorized_username)
    user_list = []
    for blocked_user in blocked:
        friendship = timelines_and_trends_actions.get_friendship(authorized_username, blocked_user['username'])
        blocked_user.update(friendship)
        user_list.append(User(blocked_user))
    return user_list


def block(authorized_username, username):
    """
                        The function add username to the blocked list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be blocked.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    check = query_factory.if_blocked(authorized_username, username)["count"]
    if check == 1:
        return "user already blocked"
    response = query_factory.block(authorized_username, username)
    if response is None:
        query_factory.unfollow(username, authorized_username)
        response = query_factory.unfollow(authorized_username, username)
    return response


def unblock(authorized_username, username):
    """
                        The function delete username from the blocked list of authorized_user if possible.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now.
                            - *username(string)*: The user to be unblocked.

                        *Returns*:
                            - *response*: indicate the successful or failure of action.
    """
    check = query_factory.if_blocked(authorized_username, username)["count"]
    if check == 0:
        return "user already unblocked"
    response = query_factory.unblock(authorized_username, username)
    return response
