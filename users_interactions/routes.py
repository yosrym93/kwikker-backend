from flask_restplus import Resource, fields
from models import User
from app import create_model
from api_namespaces import APINamespaces

interactions_api = APINamespaces.interactions_api


@interactions_api.route('/followers')
class Followers(Resource):
    @interactions_api.response(code=200, description='Followers returned successfully.', model=[User.api_model])
    @interactions_api.response(code=401, description='Unauthorized access.')
    def get(self):
        """ Retrieve a list of users that follow the authorized user. """


@interactions_api.route('/following')
class Following(Resource):
    @interactions_api.response(code=200, description='Followed users returned successfully.', model=[User.api_model])
    @interactions_api.response(code=401, description='Unauthorized access.')
    def get(self):
        """ Retrieve a list of users that are followed by the authorized user. """


@interactions_api.route('/follow')
class Follow(Resource):
    @interactions_api.response(code=201, description='User followed successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be followed.")}))
    def post(self):
        """ Follow a certain user using their username. """
        pass

    @interactions_api.response(code=204, description='User unfollowed successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unfollowed.')
    def delete(self):
        """ Unfollow a certain user using their username. """


@interactions_api.route('/blocks')
class Block(Resource):
    @interactions_api.response(code=200, description='Blocked users returned successfully.', model=[User.api_model])
    def get(self):
        """ Retrieve a list of blocked users. """

    @interactions_api.response(code=201, description='User blocked successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be blocked.")}))
    def post(self):
        """ Block a certain user using his username. """
        pass

    @interactions_api.response(code=204, description='User unblocked successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unblocked.')
    def delete(self):
        """ Unblock a certain user using his username. """


@interactions_api.route('/mutes')
class Mute(Resource):
    @interactions_api.response(code=200, description='Muted users returned successfully.', model=[User.api_model])
    def get(self):
        """ Get a list of muted users """

    @interactions_api.response(code=201, description='User muted successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match.')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.expect(create_model('Username', model={
        'username': fields.String(description="The username of the user to be muted.")}))
    def post(self):
        """ Mute a certain user using his username. """
        pass

    @interactions_api.response(code=204, description='User unmuted successfully.')
    @interactions_api.response(code=404, description='User does not exist.')
    @interactions_api.response(code=400, description='Parameters type does not match')
    @interactions_api.response(code=401, description='Unauthorized access.')
    @interactions_api.param(name='username', type='str', required=True,
                            description='The username of the user to be unmuted.')
    def delete(self):
        """ Unmute a certain user using his username. """
