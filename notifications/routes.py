from flask_restplus import Resource
from models import Notification
import api_namespaces
from . import actions
from flask import request, jsonify

notifications_api = api_namespaces.notifications_api


@notifications_api.route('/')
class Notifications(Resource):
    @notifications_api.response(code=200, description='Notifications returned successfully.',
                                model=[Notification.api_model])
    @notifications_api.response(code=401, description='Unauthorized access.')
    @notifications_api.param(name='last_notifications_retrieved_id. ', type="str", description='Nullable. Normally the '
                                                                                               'request returns the '
                                                                                               'first 20 notifications '
                                                                                               'when null. To retrieve'
                                                                                               ' more send the id of '
                                                                                               'the last retrieved'
                                                                                               ' notification.')
    @notifications_api.marshal_with(Notification.api_model, as_list=True)
    def get(self):
        """ Retrieves a list of user's notifications. """
        username = request.args.get('username')
        response = actions.get_notifications(username)
        return response, 200
