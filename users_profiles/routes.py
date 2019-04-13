from flask_restplus import Resource, fields, abort
from flask import request, send_from_directory
from models import User, UserProfile, NullableString
from app import create_model
import api_namespaces
from .import actions
from authentication_and_registration.actions import authorize
import os
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_api = api_namespaces.user_api
interactions_api = api_namespaces.interactions_api
search_api = api_namespaces.search_api


@search_api.route('/users')
class UsersSearch(Resource):
    @search_api.response(code=200, description='Users returned successfully.', model=[User.api_model])
    @search_api.response(code=400, description='Parameters type does not match.')
    @search_api.response(code=401, description='Unauthorized access.')
    @search_api.param(name='search_text', type='str', description='The text entered by the user in the search bar.')
    @search_api.param(name='last_retrieved_username', type='str',
                      description="Nullable. Normally the request returns the first 20 users when null."
                                  "To retrieve more send the username of the last user retrieved.")
    @search_api.marshal_with(User.api_model, as_list=True)
    @search_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Search for matching users using their username or screen name (or part of them). """
        search_key = request.args.get('search_text')
        username = request.args.get('last_retrieved_username')

        try:
            response = actions.search_user(authorized_username, search_key, username)
            if response is None:
                abort(404, message='A user with the provided username does not exist.')
            return response, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except ValueError:
            abort(400, 'Invalid Username provided.')


@user_api.route('/profile_banner')
class ProfileBanner(Resource):
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.response(code=204, description='Profile banner deleted.')
    @user_api.response(code=404, description='Delete failed.')
    @user_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """ Delete a profile banner (restores the default one). """
        response = actions.delete_banner_picture(authorized_username)
        if response == 'default image':
            return abort(404, message='delete request failed you can not delete default banner')
        if response == 'file does not exist':
            return abort(404, message='delete request failed file does not exist')
        if response == Exception:
            return abort(404, message=response)
        return response, 200

    @user_api.response(code=200, description='Profile banner updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.param(name='image_file', description='The new profile banner.', required=True, type='file')
    @user_api.doc(security='KwikkerKey')
    @authorize
    def put(self, authorized_username):
        """ Update a profile banner given the new banner image. """
        if 'file' not in request.files:
            return abort(404, message='No image part')
        file = request.files['file']
        response = actions.update_profile_banner(file, authorized_username)
        if response == 'No selected file':
            return abort(404, message=response)
        if response == 'not allowed extensions':
            return abort(404, message=response)
        if response == Exception:
            return abort(404, message=response)
        return response, 200


@user_api.route('/profile_picture')
class ProfilePicture(Resource):
    @user_api.response(code=204, description='Profile picture deleted.')
    @user_api.response(code=404, description='Delete failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """ Delete a profile picture (restores the default one). """
        response = actions.delete_profile_picture(authorized_username)
        if response == 'default image':
            return abort(404, message='delete request failed you can not delete default profile picture')
        if response == 'file does not exist':
            return abort(404, message='delete request failed file does not exist')
        if response == Exception:
            return abort(404, message=response)
        return response, 200

    @user_api.response(code=200, description='Profile picture updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.param(name='image_file', description='The new profile picture.', required=True, type='file')
    @user_api.doc(security='KwikkerKey')
    @authorize
    def put(self, authorized_username):
        """ Update a profile picture given the new picture. """
        if 'file' not in request.files:
            return abort(404, message='No image part')
        file = request.files['file']
        response = actions.update_profile_picture(file, authorized_username)
        if response == 'No selected file':
            return abort(404, message=response)
        if response == 'not allowed extensions':
            return abort(404, message=response)
        if response == Exception:
            return abort(404, message=response)
        return response, 200


@user_api.route('/upload/picture/<filename>')
class PhotoUploadP(Resource):
    @staticmethod
    def get(filename):
        os.chdir(os.path.dirname(APP_ROOT))
        return send_from_directory('images\profile', filename)


@user_api.route('/upload/banner/<filename>')
class PhotoUploadB (Resource):
    @staticmethod
    def get(filename):
        os.chdir(os.path.dirname(APP_ROOT))
        return send_from_directory('images\\banner', filename)


@user_api.route('/profile')
class UserProfile(Resource):
    @user_api.response(code=200, description='Profile updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.expect(create_model('Profile', model={
        'bio': NullableString(description='Nullable if unchanged. The biography of the user.'),
        'screen_name': NullableString(description='Nullable if unchanged. The name shown on profile screen.')
    }), validate=True)
    @user_api.doc(security='KwikkerKey')
    @authorize
    def patch(self, authorized_username):
        """ Update the biography or screen name in user profile."""
        data = request.get_json()
        bio = data.get('bio')
        screen_name = data.get('screen_name')
        response = actions.update_user_profile(authorized_username, bio, screen_name)
        if response == - 1:
            abort(404, message='update failed.')
        if response == 0:
            return abort(400, 'pay load is empty or equal to null no update happened')
        return 'profile updated', 200

    @user_api.response(code=200, description='User profile returned successfully.', model=UserProfile.api_model)
    @user_api.response(code=404, description='User does not exist.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.marshal_with(UserProfile.api_model, as_list=True)
    @user_api.param(name='username', type='str', required=True, description='The username.')
    @user_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieve the profile of a specific user. """
        username = request.args.get('username')
        response = actions.get_user_profile(authorized_username, username)
        if response == - 1:
            return abort(404, message='User does not exist.')
        if response == Exception:
            return abort(409, message='conflict happened.')
        return response, 200
