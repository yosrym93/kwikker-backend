from flask_restplus import Namespace, Resource, fields
from models import User, Kweek
from app import create_model

example_api = Namespace('example')


@example_api.route('/secondary')
class ExampleResource(Resource):
    @example_api.response(code=200, description='User returned successfully', model=User.api_model)
    @example_api.response(code=404, description='X not found')
    @example_api.param(name='id', type='int', description='The id')
    @example_api.param(name='username', type='str', description='The username')
    def get(self):
        pass

    @example_api.response(code=200, description='Logged in successfully')
    @example_api.response(code=404, description='User does not exist')
    @example_api.expect(create_model('Login Form', model={
        'username': fields.String,
        'password': fields.String
    }))
    def post(self):
        pass

    @example_api.expect(Kweek.api_model)
    def put(self):
        pass
