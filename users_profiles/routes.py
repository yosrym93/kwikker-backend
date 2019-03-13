from flask_restplus import Resource, fields
from models import User, UserProfile
from app import create_model
import api_namespaces

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
    def get(self):
        """ Search for matching users using their username or screen name (or part of them). """
        pass


@user_api.route('/profile_banner')
class ProfileBanner(Resource):
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.response(code=200, description='Profile banner deleted.')
    @user_api.response(code=404, description='Delete failed.')
    def delete(self,):
        """ Delete a profile banner (restores the default one). """
        pass

    @user_api.response(code=200, description='Profile banner updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.param(name='image_file', description='The new profile banner.', type='file')
    def put(self):
        """ Update a profile banner given the new banner image. """
        pass


@user_api.route('/profile_picture')
class ProfilePicture(Resource):
    @user_api.response(code=200, description='Profile picture deleted.')
    @user_api.response(code=404, description='Delete failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    def delete(self,):
        """ Delete a profile picture (restores the default one). """
        pass

    @user_api.response(code=200, description='Profile picture updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.param(name='image_file', description='The new profile picture.', type='file')
    def put(self):
        """ Update a profile picture given the new picture. """
        pass


@user_api.route('/profile')
class UserProfile(Resource):
    @user_api.response(code=200, description='Profile updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.expect(create_model('Profile', model={
        'bio': fields.String(description='Nullable if unchanged. The biography of the user.'),
        'screen_name': fields.String(description='Nullable if unchanged. The name shown on profile screen.')
    }))
    def patch(self):
        """ Update the biography or screen name in user profile."""
        pass

    @user_api.response(code=200, description='User profile returned successfully.', model=UserProfile.api_model)
    @user_api.response(code=404, description='User does not exist.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.response(code=400, description='Parameters type does not match.')
    @user_api.param(name='username', type='str', description='The username.')
    def get(self):
        """ Retrieve the profile of a specific user. """
        pass


@user_api.route('/email')
class ChangeEmail(Resource):
    @user_api.response(code=200, description='Email updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.expect(create_model('New Email', model={
     'email': fields.String(description="User's new email.")}))
    def put(self):
        """ Update email of the authorized user. """
        pass


@user_api.route('/username')
class ChangeUsername(Resource):
    @user_api.response(code=200, description='Username updated.')
    @user_api.response(code=404, description='Update failed')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.expect(create_model('New Username', model={
        'username': fields.String(description="User's new username")}))
    def put(self):
        """ Update username of the authorized user. """
        pass


@user_api.route('/password')
class ChangePassword(Resource):
    @user_api.response(code=200, description='Password updated.')
    @user_api.response(code=404, description='Update failed.')
    @user_api.response(code=401, description='Unauthorized access.')
    @user_api.expect(create_model('New Password', model={
        'password': fields.String(description="User's new password.")}))
    def put(self):
        """ Update password of the authorized user. """
        pass
