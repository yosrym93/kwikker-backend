from flask_restplus import Resource, fields, abort
from flask import request
from models import User, UserProfile
from app import create_model
from timelines_and_trends import actions as trends_actions
from authentication_and_registration.actions import authorize
from .import actions
import api_namespaces

interactions_api = api_namespaces.interactions_api


@interactions_api.route('/followers')
class Followers(Resource):
    @interactions_api.response(code=200, description='Followers returned successfully.', model=[UserProfile.api_model])
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True, description='The username.')
    @interactions_api.param(name='last_retrieved_username', type='str', required=True, description="Nullable. Normally the request returns the first 20 users when null."
                            "To retrieve more send the username of the last user retrieved.")
    @interactions_api.marshal_with(UserProfile.api_model, as_list=True)
    def get(self):
        """ Retrieve a list of users that follow the username. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        else:
            username = request.args.get('username')
            last_retrieved_username = request.args.get('last_retrieved_username')
            if not trends_actions.is_user(username):
                abort(404, message='A user with this username does not exist.')
            try:
                followers_list = actions.get_profile_followers(username=username, last_retrieved_username=last_retrieved_username)
                if followers_list is None:
                    abort(404, message='A user with the provided last_retrieved_username does not exist.')
                return followers_list, 200
            except TypeError:
                abort(500, message='An error occurred in the server.')
            except ValueError:
                abort(400, 'Invalid username provided.')


@interactions_api.route('/following')
class Following(Resource):
    @interactions_api.response(code=200, description='Followed users returned successfully.', model=[UserProfile.api_model])
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True, description='The username.')
    @interactions_api.param(name='last_retrieved_username', type='str', required=True,
                            description="Nullable. Normally the request returns the first 20 users when null."
                                        "To retrieve more send the username of the last user retrieved.")
    @interactions_api.marshal_with(UserProfile.api_model, as_list=True)
    def get(self):
        """ Retrieve a list of users that are followed by the username. """

        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        else:
            username = request.args.get('username')
            last_retrieved_username = request.args.get('last_retrieved_username')
            if not trends_actions.is_user(username):
                abort(404, message='A user with this username does not exist.')
            try:
                following_list = actions.get_profile_following(username=username,
                                                               last_retrieved_username=last_retrieved_username)
                if following_list is None:
                    abort(404, message='A user with the provided last_retrieved_username does not exist.')
                return following_list, 200
            except TypeError:
                abort(500, message='An error occurred in the server.')
            except ValueError:
                abort(400, 'Invalid username provided.')


@interactions_api.route('/follow')
class Follow(Resource):
    @interactions_api.response(code=201, description='User followed successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be followed.")}))
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Follow a certain user using their username. """
        data = request.get_json()
        username = data.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not follow your self')
        response = actions.follow(username=username, authorized_username=authorized_username)
        if response is None:
            return 'User followed successfully', 200
        return response, 400

    @interactions_api.response(code=204, description='User unfollowed successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unfollowed.')
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """ Unfollow a certain user using their username. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        username = request.args.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not unfollow your self')
        response = actions.unfollow(username=username, authorized_username=authorized_username)
        if response is None:
            return 'User unfollowed successfully', 200
        return response, 400


@interactions_api.route('/blocks')
class Block(Resource):
    @interactions_api.response(code=200, description='Blocked users returned successfully.', model=[User.api_model])
    @interactions_api.marshal_with(User.api_model, as_list=True)
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieve a list of blocked users. """
        response = actions.get_blocked_users(authorized_username)
        return response

    @interactions_api.response(code=201, description='User blocked successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be blocked.")}))
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Block a certain user using his username. """
        data = request.get_json()
        username = data.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not block your self.')
        response = actions.block(authorized_username=authorized_username, username=username)
        if response is None:
            return "user is blocked successfully", 200
        return response, 400

    @interactions_api.response(code=204, description='User unblocked successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unblocked.')
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """ Unblock a certain user using his username. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        username = request.args.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not unblocked your self.')
        response = actions.unblock(authorized_username=authorized_username, username=username)
        if response is None:
            return "user is unblocked successfully", 200
        return response, 400


@interactions_api.route('/mutes')
class Mute(Resource):
    @interactions_api.response(code=200, description='Muted users returned successfully.', model=[User.api_model])
    @interactions_api.marshal_with(User.api_model, as_list=True)
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Get a list of muted users """
        response = actions.get_muted_users(authorized_username)
        return response

    @interactions_api.response(code=201, description='User muted successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be muted.")}))
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Mute a certain user using his username. """
        data = request.get_json()
        print(data)
        username = data.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not mute your self.')
        response = actions.mute(authorized_username=authorized_username, username=username)
        if response is None:
            return "user is muted successfully", 200
        return response, 400

    @interactions_api.response(code=204, description='User unmuted successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unmuted.')
    @interactions_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """ Unmute a certain user using his username. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        username = request.args.get('username')
        if not trends_actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        if username == authorized_username:
            abort(400, message='A bad request can not unmute your self.')
        response = actions.unmute(authorized_username=authorized_username, username=username)
        if response is None:
            return "user is unmuted successfully", 200
        return response, 400

