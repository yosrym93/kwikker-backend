from flask_restplus import Namespace, Resource

account_api = Namespace('account')

'''
    Use @account_api  instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@account_api.route('/')
class Example(Resource):
    pass
