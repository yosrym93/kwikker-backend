from flask_restplus import Resource, abort, fields
from models import Notification
from app import create_model
import api_namespaces
from . import actions
from flask import request
from authentication_and_registration.actions import authorize

notifications_api = api_namespaces.notifications_api


@notifications_api.route('/')
class Notifications(Resource):
    @notifications_api.response(code=200, description='Notifications returned successfully.',
                            model=create_model('Notifications', model={
                                'unseen_count': fields.Integer('The number of unseen notifications.'),
                                'Notifications': fields.List(fields.Nested(Notification.api_model))
                            }))
    @notifications_api.response(code=401, description='Unauthorized access.')
    @notifications_api.response(code=404, description="Notification id does not exist.")
    @notifications_api.response(code=500, description='An error occurred in the server.')
    @notifications_api.response(code=400, description='Invalid ID provided.')
    @notifications_api.param(name='last_notification_retrieved_id', type="str",
                             description='Nullable. Normally the request returns the first 20 notifications when null. '
                                         'To retrieve more send the id of the last retrieved notification.')
    @notifications_api.marshal_with(create_model('Notifications', model={
                                'unseen_count': fields.Integer('The number of unseen notifications.'),
                                'Notifications': fields.List(fields.Nested(Notification.api_model))
                                }))
    @notifications_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of user's notifications. """
        last_notification_retrieved_id = request.args.get('last_notification_retrieved_id')
        try:
            notifications = actions.get_notifications(authorized_username, last_notification_retrieved_id)
            if notifications is None:
                abort(404, message='A notification with the provided ID does not exist.')
            else:
                if len(notifications) == 0:
                    return {
                        'unseen_count': 0,
                        'Notifications': []
                    }
                unseen_count = actions.get_notifications_unseen_count(authorized_username)
                actions.set_notifications_as_seen(authorized_username)
                return {
                    'unseen_count': unseen_count,
                    'Notifications': notifications
                }
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except ValueError:
            abort(400, message='Invalid ID provided.')


# @notifications_api.route('/TEST')
# class Notifications(Resource):
#     def get(self):
#         try:
#             actions.create_notifications('ahly', 'zamalek', 'LIKE')
#         except Exception as e:
#
#             print(e)
#             if e == Exception('Involved_username does not exist'):
#                 print(1)