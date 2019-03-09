from flask_restplus import Namespace, Resource

kweeks_api = Namespace('kweeks')
media_api = Namespace('media')

'''
    Use @kweeks_api and @media_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@kweeks_api.route('/')
class Example(Resource):
    pass
