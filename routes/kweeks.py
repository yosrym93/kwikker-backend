from flask_restplus import Namespace, Resource

kweeks_api = Namespace(name='Kweeks', path='/kweeks')
media_api = Namespace(name='Media', path='/media')

'''
    Use @kweeks_api and @media_api instead of api
    Replace the following class with your resources
'''


# TODO: Write the documented endpoints
@kweeks_api.route('/')
class Example(Resource):
    pass
