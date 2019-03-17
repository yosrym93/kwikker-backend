from . import query_factory
from timelines_and_trends import actions
from models import UserProfile
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
"""
    All the functions containing the logic should reside here. 
    The routes functions should contain no logic, they should only call the functions in this module.
"""


def get_user_profile(authorized_username, username):
    profile = query_factory.get_user_profile(username)
    if profile:
        profile["profile_image_url"] = 'http://127.0.0.1:5000/user/upload/picture/' + profile[
            "profile_image_url"]
        profile["profile_banner_url"] = 'http://127.0.0.1:5000/user/upload/banner/' + profile[
            "profile_banner_url"]
        profile["followers_count"] = query_factory.get_user_followers(username)["count"]
        profile["following_count"] = query_factory.get_user_following(username)["count"]
        profile["kweeks_count"] = query_factory.get_number_of_kweeks(username)['count']
        profile["likes_count"] = query_factory.get_number_of_likes(username)['count']
        friendship = actions.get_friendship(authorized_username, username)
        profile.update(friendship)
        return UserProfile(profile)
    else:
        return -1


def update_user_profile(username, bio, screen_name):

    if bio == "" and screen_name == "":
        return 0
    if bio is not None or screen_name is not None:

        response = query_factory.update_user_profile(username, bio, screen_name)
        if response is None:
            return response
        else:
            return -1
    else:
        return 0


def update_profile_picture(file, username):
    target = os.path.join(APP_ROOT, 'images\profile/')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = username + 'profile.png'
    response = query_factory.update_user_profile_picture(username, filename)
    if response is None:
        destination = "/".join([target, filename])
        file.save(destination)
        return filename

    else:
        return -1


def delete_profile_picture(username):
    filename = 'profile.jpg'
    response = query_factory.update_user_profile_picture(username, filename)
    if response is None:
        return

    else:
        return -1


def update_profile_banner(file, username):
    target = os.path.join(APP_ROOT, 'images\ banner/')
    if not os.path.isdir(target):
        os.mkdir(target)
    filename = username + 'banner.png'
    response = query_factory.update_user_banner_picture(username, filename)
    if response is None:
        destination = "/".join([target, filename])
        file.save(destination)
        return filename
    else:
        return -1


def delete_banner_picture(username):
    filename = 'banner.png'
    response = query_factory.update_user_banner_picture(username, filename)
    if response is None:
        return

    else:
        return -1
