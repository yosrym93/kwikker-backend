from flask_restplus import Namespace, Resource

messages_api = Namespace('direct_message')
notifications_api = Namespace('notifications')

'''
    Use @messages_api and @notifications_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@messages_api.route('/')
class Example(Resource):
    pass
