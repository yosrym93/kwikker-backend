from flask_restplus import Namespace, Resource
from .login_registration import account_api
from .timelines import search_api

user_api = Namespace('user')
interactions_api = Namespace('interactions')

'''
    Use @user_api, @search_api, @interactions and @account_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@interactions_api.route('/')
class Example(Resource):
    pass
