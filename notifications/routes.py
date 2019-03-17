from flask_restplus import Resource, abort
from models import Notification
import api_namespaces
from . import actions
from flask import request

notifications_api = api_namespaces.notifications_api


@notifications_api.route('/')
class Notifications(Resource):
    @notifications_api.response(code=200, description='Notifications returned successfully.',
                                model=[Notification.api_model])
    @notifications_api.response(code=401, description='Unauthorized access.')
    @notifications_api.response(code=404, description="User does not exist.")
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
        if not actions.is_user(username):
            abort(404, message='A user with this username does not exist.')
        notifications = actions.get_notifications(username)
        if len(notifications) == 0:
            return [], 200
        return notifications, 200
