from flask_restplus import Namespace, Resource
from .kweeks import kweeks_api

trends_api = Namespace(name='Trends', path='/trends')
search_api = Namespace(name='Search', path='/search')

'''
    Use @kweeks_api, @search_api and @trends_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@kweeks_api.route('/')
class Example(Resource):
    pass
