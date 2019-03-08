from flask_restplus import Namespace, Resource
from models import User, Kweek

example_api = Namespace('example')


@example_api.route('/secondary')
class ExampleResource(Resource):
    @example_api.response(code=200, description='User returned successfully', model=User.api_model)
    @example_api.response(code=404, description='X not found')
    @example_api.param(name='id', type='int', description='The id')
    @example_api.param(name='username', type='str', description='The username')
    def get(self):
        pass

    @example_api.expect(Kweek.api_model)
    def post(self):
        pass
