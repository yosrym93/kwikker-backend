from flask_restplus import Namespace, Resource
from .kweeks import kweeks_api

trends_api = Namespace('trends')
search_api = Namespace('search')

'''
    Use @kweeks_api, @search_api and @trends_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@kweeks_api.route('/')
class Example(Resource):
    pass
