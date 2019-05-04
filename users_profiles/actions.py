from . import query_factory
from timelines_and_trends import actions
from users_interactions import query_factory as user_interaction_query_factory
from models import UserProfile
import datetime
from app import app
import os
import fnmatch

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
Server_path = app.config['SERVER_PATH']
size = 20


def create_url(upload_type, filename, add_dummy_value=False):
    """
                    The function return url of profile image .
                    *Parameters*:
                        - *upload_type (str)*: The type of upload banner or picture.
                        - *filename (str)*: The name of the profile image.
                    *Returns*:
                        - url of profile image .
    """
    url = Server_path + 'user/upload/' + upload_type + '/' + filename
    if add_dummy_value:
        url += '?'
        url += ''.join(c for c in str(datetime.datetime.utcnow()) if c.isalnum())
    return url


def allowed_file(filename):
    """
                                The function checks if the uploaded file has allowed extension.

                                *Parameters*:
                                    - *filename*: The name of the uploaded file .
                                *Returns*:
                                    - *True or False*: in the allowed extension or not.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_user_profile(authorized_username, username):
    """
            The function return user profile for a specific user.

            *Parameters*:
                - *authorized_username (string)*: The user that is logged in now.
                - *username (string)*: The user that we will test friendship on it like (following ..)

            *Returns*:
                - *UserProfile*: an object of user profile .
    """
    if username is None:
        return -1
    check_user = actions.is_user(username)
    if not check_user:
        return -1
    profile = query_factory.get_user_profile(username)
    check_block = user_interaction_query_factory.if_blocked(username, authorized_username)['count']
    if check_block == 1:
        dict_blocked = {'username': profile['username'], 'screen_name': profile['screen_name'],
                        'profile_image_url': profile['profile_image_url'],
                        'profile_banner_url': profile['profile_banner_url']}
        return dict_blocked
    profile["followers_count"] = query_factory.get_user_followers(username)["count"]
    profile["following_count"] = query_factory.get_user_following(username)["count"]
    profile["kweeks_count"] = query_factory.get_number_of_kweeks(username)['count']
    profile["likes_count"] = query_factory.get_number_of_likes(username)['count']
    friendship = actions.get_friendship(authorized_username, username)
    profile.update(friendship)
    return UserProfile(profile)


def create_profile(username, screen_name, birth_date):
    """
                The function creates new profile in database.

                *Parameters*:
                    - *username (string)*: The username .
                    - *screen_name*: screen_name.
                    -*birth_date*: date of birth.
                *Returns*:
                    - *True*: profile created successfully.
                    - *False*: if profile is already created or database error .
    """
    if username is None or username == "":
        return False
    check_user = actions.is_user(username)
    if not check_user:
        return False
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response = query_factory.create_profile(username, screen_name, birth_date, time,
                                            profile_image_url=create_url('picture', 'profile.jpg'),
                                            banner_url=create_url('banner', 'banner.jpg'))
    if response is None:
        return True
    return False


def update_user_profile(authorized_username, bio, screen_name):
    """
                The function updates bio and screen name in user profile.

                *Parameters*:
                    - *authorized_username (string)*: The user that is logged in now .
                    - *bio (text)*: The biography of the user.
                    - *screen_name(string)*: The name shown on profile screen.
                *Returns*:
                    - *response*: which is none of case in successful update .
                    - *-1*: in case of exception error in database.
                    - *0*: in case of bad request.
    """
    if (bio == "" or bio is None) and (screen_name == "" or screen_name is None):
        return 0
    response = query_factory.update_user_profile(authorized_username, bio, screen_name)
    return response


def update_profile_picture(file, authorized_username):  # pragma:no cover
    """
                    The function updates profile picture.

                    *Parameters*:
                        - *file (file)*: The profile image which will be updated.
                        - *authorized_username (string)*: The user that is logged in now .
                    *Returns*:
                        - *filename*: the image name saved in database .
    """
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):

        images = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(images):
            os.mkdir(images)
        target = os.path.join(APP_ROOT, 'images/profile/')

        if not os.path.isdir(target):
            os.mkdir(target)

        filename, ext = os.path.splitext(file.filename)
        filename = authorized_username + 'profile' + ext
        response = query_factory.update_user_profile_picture(authorized_username, create_url('picture', filename,
                                                                                             add_dummy_value=True))
        if response is None:
            destination = "/".join([target, filename])
            file.save(destination)
            return create_url('picture', filename, add_dummy_value=True)

        else:
            return response
    else:
        return 'not allowed extensions'


def delete_profile_picture(authorized_username):
    """
                            The function deletes profile picture and reset it to default.

                            *Parameters*:
                                - *authorized_username (string)*: The user that is logged in now .
                            *Returns*:
                                - *response*: which is none of case in successful deletion .
    """

    default_filename = 'profile.jpg'
    default_path = create_url('picture', default_filename)
    filename = query_factory.get_user_profile_picture(authorized_username)['profile_image_url']
    if filename == default_path:
        return 'default image'
    filename = filename[:-21]  # Remove the ? and the dummy value from the end of the url
    filename = filename.rsplit('/', 1)
    filename = filename[1]
    path = APP_ROOT + '/images/profile'
    response = query_factory.update_user_profile_picture(authorized_username, default_path)
    if response is None:
        os.chdir(path)
        if os.path.exists(filename):
            os.remove(filename)
            return create_url('picture', 'profile.jpg')
        else:
            return 'file does not exist'
    else:
        return response  # pragma:no cover


def update_profile_banner(file, authorized_username):  # pragma:no cover
    """
                        The function updates banner picture.

                        *Parameters*:
                            - *file (file)*: The banner image which will be updated.
                            - *authorized_username (string)*: The user that is logged in now .
                        *Returns*:
                            - *filename*: the image name saved in database .
    """
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        images = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(images):
            os.mkdir(images)
        target = os.path.join(APP_ROOT, 'images/banner/')

        if not os.path.isdir(target):
            os.mkdir(target)

        filename, ext = os.path.splitext(file.filename)  # ------------------------
        filename = authorized_username + 'banner' + ext
        response = query_factory.update_user_banner_picture(authorized_username, create_url('banner', filename,
                                                                                            add_dummy_value=True))
        if response is None:
            destination = "/".join([target, filename])
            file.save(destination)
            return create_url('banner', filename,
                              add_dummy_value=True)

        else:
            return response
    else:
        return 'not allowed extensions'


def delete_banner_picture(authorized_username):
    """
                        The function deletes banner picture and reset it to default.

                        *Parameters*:
                            - *authorized_username (string)*: The user that is logged in now .
                        *Returns*:
                            - *response*: which is none of case in successful deletion .
    """
    default_filename = 'banner.jpg'
    default_path = create_url('banner', default_filename)
    filename = query_factory.get_user_banner_picture(authorized_username)['profile_banner_url']
    if filename == default_path:
        return 'default image'
    filename = filename[:-21]  # Remove the ? and the dummy value from the end of the url
    filename = filename.rsplit('/', 1)
    filename = filename[1]
    path = APP_ROOT + '/images/banner'
    response = query_factory.update_user_banner_picture(authorized_username, default_path)
    if response is None:
        os.chdir(path)
        if os.path.exists(filename):
            os.remove(filename)
            return create_url('banner', 'banner.jpg')
        else:
            return 'file does not exist'
    else:
        return response  # pragma:no cover


def search_user(authorized_username, search_key, username, results_size=size):
    """
                The function returns a list of users searched by search_key.

                *Parameters*:
                    - *authorized_username (string)*: The user that is logged in now.
                    - *search_key (string)*: The keyword used to get best match users.
                    - *username (string)*: The last username retrieve. Results after this one are fetched.

                *Returns*:
                    - *User_list*: a list of objects of user_profile.
    """
    if search_key == "":
        return []
    results = query_factory.search_user(search_key)
    try:
        results = actions.paginate(dictionaries_list=results, required_size=results_size,
                                   start_after_key='username', start_after_value=username)
    except TypeError as E:
        print(E)
        raise
    if results is None:
        return None
    user_list = []
    for result in results:
        result["followers_count"] = query_factory.get_user_followers(result['username'])["count"]
        result["following_count"] = query_factory.get_user_following(result['username'])["count"]
        result["kweeks_count"] = query_factory.get_number_of_kweeks(result['username'])['count']
        result["likes_count"] = query_factory.get_number_of_likes(result['username'])['count']
        friendship = actions.get_friendship(authorized_username, result['username'])
        result.update(friendship)
        user_list.append(UserProfile(result))
    return user_list


def update_profile_images_on_username_update(old_username, new_username):  # pragma:no cover
    """
            Updates the file names and the urls of the profile and banner pictures of the user on username change.

            *Parameters*:
                - *old_username (string)*: The old username of the user.
                - *new_username (string)*: The new username of the user.

            *Returns*:
                - *False*: If updating the url in the database yielded an error.
                - *True*: Otherwise.
    """
    # Update URL in database
    # Profile image url
    profile_image_url = query_factory.get_user_profile_picture(new_username)['profile_image_url']
    fixed_url_part = Server_path + 'user/upload/profile/'
    file_name = profile_image_url[len(fixed_url_part):]
    default_file_name = 'profile.jpg'
    if file_name != default_file_name:
        file_name = file_name[:-21]  # Remove the ? and the dummy value from the end of the url
        dummy, ext = os.path.splitext(file_name)
        new_file_name = new_username + 'profile' + ext
        query_factory.update_user_profile_picture(new_username, create_url('picture', new_file_name,
                                                                           add_dummy_value=True))

    # Banner image url
    banner_image_url = query_factory.get_user_banner_picture(new_username)['profile_banner_url']
    fixed_url_part = Server_path + 'user/upload/banner/'
    file_name = banner_image_url[len(fixed_url_part):]
    default_file_name = 'banner.jpg'
    if file_name != default_file_name:
        file_name = file_name[:-21]  # Remove the ? and the dummy value from the end of the url
        dummy, ext = os.path.splitext(file_name)
        new_file_name = new_username + 'banner' + ext
        query_factory.update_user_banner_picture(new_username, create_url('banner', new_file_name,
                                                                          add_dummy_value=True))

    # Update the profile image file name
    search_path = os.path.join(APP_ROOT, 'images/profile')
    filename = old_username + 'profile' + '.*'
    new_filename = new_username + 'profile'
    for root, dirs, files in os.walk(search_path):
        for name in files:
            if fnmatch.fnmatch(name, filename):
                print(name, 'filename')
                dummy, ext = os.path.splitext(name)
                os.rename(search_path + '/' + name, search_path + '/' + new_filename + ext)

    # Update the banner image file name
    search_path = os.path.join(APP_ROOT, 'images/banner')
    filename = old_username + 'banner' + '.*'
    new_filename = new_username + 'banner'
    for root, dirs, files in os.walk(search_path):
        for name in files:
            if fnmatch.fnmatch(name, filename):
                dummy, ext = os.path.splitext(name)
                os.rename(search_path + '/' + name, search_path + '/' + new_filename + ext)

    return True
