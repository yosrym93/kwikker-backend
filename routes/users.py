from flask_restplus import Namespace, Resource, fields
from models import User,UserProfile
from app import create_model
user_api = Namespace(name='User', path='/user',description='change account setting,banner,profile picture '
                                                           'and search for users')
interactions_api = Namespace(name='Interactions', path='/interactions',
                             description='Following, muting, and blocking')

'''
    Use @user_api, @search_api, @interactions and @account_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@user_api.route('/search')
class GetUsers(Resource):
    @user_api.response(code=200, description='User returned successfully', model=[User.api_model])
    @user_api.response(code=404, description='user not found')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.param(name='username', type='str', description='The username or part of it. ')
    def get(self):
        """ Search for matching users using their usernames or part of it """
        pass


@user_api.route('/')
class GetUserProfile(Resource):
    @user_api.response(code=200, description='User Profile returned successfully', model=UserProfile.api_model)
    @user_api.response(code=404, description='user not found')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.param(name='username', type='str', description='The username.')
    def get(self):
        """ Search for specific users using their usernames  """
        pass


@user_api.route('/profile_banner')
class ProfileBanner(Resource):
    @user_api.response(code=204, description='profile_banner deleted')
    @user_api.response(code=404, description='delete failed')
    def delete(self,):
        """ Delete a profile banner. """
        pass

    @user_api.response(code=204, description='profile_banner updated')
    @user_api.response(code=404, description='update failed')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.param(name='image file', description='The new profile banner', type='file')
    def put(self):
        """ update a profile banner given the new banner. """
        pass


@user_api.route('/profile_picture')
class ProfilePicture(Resource):
    @user_api.response(code=204, description='profile_picture deleted')
    @user_api.response(code=404, description='delete failed')
    def delete(self,):
        """ Delete a profile picture. """
        pass

    @user_api.response(code=204, description='profile_picture updated')
    @user_api.response(code=404, description='update failed')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.param(name='image file', description='The new profile picture', type='file')
    def put(self):
        """ update a profile picture given the new picture. """
        pass


@user_api.route('/profile')
class ProfileSettings(Resource):
    @user_api.response(code=200, description='profile updated')
    @user_api.response(code=404, description='update failed')
    @user_api.expect(create_model('Profile', model={
        'bio': fields.String(description='the biography of the user', nullable=True),
        'screen_name': fields.String(description='the name shown on profile screen.', nullable=True)
    }))
    def patch(self):
        """Update bio or screen name in user profile."""
        pass


@user_api.route('/email')
class ChangeEmail(Resource):
    @user_api.response(code=200, description='email updated')
    @user_api.response(code=404, description='update failed')
    @user_api.expect(create_model('NewEmail', model={
     'email':fields.String(description="user new email")}))
    def put(self):
        """ update email of a user. """
        pass


@user_api.route('/username')
class ChangeUserName(Resource):
    @user_api.response(code=200, description='username updated')
    @user_api.response(code=404, description='update failed')
    @user_api.expect(create_model('NewUsername', model={
        'username': fields.String(description="user new username")}))
    def put(self):
        """ update username of a user. """
        pass


@user_api.route('/password')
class ChangePassword(Resource):
    @user_api.response(code=200, description='Password updated')
    @user_api.response(code=404, description='update failed')
    @user_api.expect(create_model('NewPassword', model={
        'password': fields.String(description="user new Password")}))
    def put(self):
        """ update password of a user. """
        pass


@interactions_api.route('/followers')
class GetFollowers(Resource):
    @user_api.response(code=200, description='List returned successfully', model=[User.api_model])
    @user_api.response(code=404, description='List is not exist ')
    def get(self):
        """get a list of users that follow me"""


@interactions_api.route('/following')
class GetFollowing(Resource):
    @user_api.response(code=200, description='List returned successfully', model=[User.api_model])
    @user_api.response(code=404, description='List is not exist ')
    def get(self):
        """get a list of users that i am follow"""


@interactions_api.route('/follow')
class FollowUnfollow(Resource):
    @user_api.response(code=201, description='Successful request user added to following list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to follow")}))
    def post(self):
        """ follow a certain user using his username . """
        pass

    @user_api.response(code=201, description='Successful request user removed from following list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to unfollow")}))
    def delete(self):
        """ unfollow a certain user using his username . """


@interactions_api.route('/blocks')
class BlockUnblock(Resource):

    @user_api.response(code=200, description='List returned successfully', model=[User.api_model])
    @user_api.response(code=404, description='List is not exist ')
    def get(self):
        """get a list of blocked users"""

    @user_api.response(code=201, description='Successful request user added to blocked list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to block")}))
    def post(self):
        """ block a certain user using his username . """
        pass

    @user_api.response(code=201, description='Successful request user removed from blocked list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to unblock")}))
    def delete(self):
        """ unblock a certain user using his username . """


@interactions_api.route('/mutes')
class BlockUnblock(Resource):

    @user_api.response(code=200, description='List returned successfully', model=[User.api_model])
    @user_api.response(code=404, description='List is not exist ')
    def get(self):
        """get a list of muted users"""

    @user_api.response(code=201, description='Successful request user added to muted list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to mute")}))
    def post(self):
        """ mute a certain user using his username . """
        pass

    @user_api.response(code=201, description='Successful request user removed from muted list')
    @user_api.response(code=404, description='Failed request ')
    @user_api.response(code=400, description='parameters type does not match')
    @user_api.expect(create_model('Username', model={
        'username': fields.String(description="the user that i want to mute")}))
    def delete(self):
        """ unmute a certain user using his username . """

