from flask_restplus import Resource, fields
from app import create_model
from models import Kweek, User
from api_namespaces import APINamespaces

kweeks_api = APINamespaces.kweeks_api


@kweeks_api.route('/')
class Kweeks(Resource):
    @kweeks_api.expect(create_model('Created Kweek', {
                                        'kweek_text': fields.String,
                                        'reply_to': fields.String(description='The id of the kweek that this kweek '
                                                                              'is a reply to. Null if the kweek is not'
                                                                              ' a reply.')
                                    }))
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=201, description='Kweek created successfully.')
    def post(self):
        """
        Create a new Kweek or reply.
        """
        pass

    @kweeks_api.response(code=200, description='Kweek has been deleted successfully.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='str', description='The id of the Kweek to be deleted.', required=True)
    def delete(self):
        """
        Delete an existing Kweek.
        """
        pass

    @kweeks_api.response(code=200, description='Kweek has been returned successfully.',
                         model=create_model('Kweek & Replies',
                                            model={'Kweek': fields.Nested(Kweek.api_model,
                                                                          description='The returned Kweek.'),
                                                   'replies': fields.List(fields.Nested(Kweek.api_model,
                                                                                        description='Direct replies '
                                                                                                    'of the Kweek'))}))
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='id', type='str', description='Id of the Kweek to be retrieved', required=True)
    def get(self):
        """
        Retrieve a Kweek with its replies.
        """
        pass


@kweeks_api.route('/replies')
class KweekReplies(Resource):
    @kweeks_api.response(code=200, description='Replies have been returned successfully.',
                         model=[Kweek.api_model])
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='reply_to', type='str',
                      description='Id of the Kweek that the replies belong to.', required=True)
    def get(self):
        """
        Retrieve replies of a Kweek.
        """
        pass


@kweeks_api.route('/rekweek')
class Rekweek(Resource):
    @kweeks_api.expect(create_model('Kweek ID', {
        'id': fields.String(description='The id of the kweek to be liked.')
    }))
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=201, description='Reweek created successfully')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    def post(self):
        """
        Create a new Rekweek.
        """
        pass

    @kweeks_api.response(code=200, description='Rekweek has been deleted successfully.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='string', description='Id of the rekweek to be deleted', required=True)
    def delete(self):
        """
        Delete an existing rekweek.
        """
        pass


@kweeks_api.route('/rekweekers')
class KweekRekweekers(Resource):
    @kweeks_api.response(code=200, description='Rekweerkers have been returned successfully.',
                         model=[User.api_model])
    @kweeks_api.param(name='id', type='str',
                      description='Id of the Kweek whose rekweekers are to be retrieved', required=True)
    def get(self):
        """
        Retrieve rekweekers of a kweek.
        """
        pass


@kweeks_api.route('/likers')
class KweekLikers(Resource):
    @kweeks_api.response(code=200, description='Likers have been returned successfully.',
                         model=[User.api_model])
    @kweeks_api.param(name='id', type='string', description='The kweek id to be liked', required=True)
    def get(self):
        """
        Retrieve likers of a kweek .
        """
        pass


@kweeks_api.route('/like')
class Like(Resource):
    @kweeks_api.response(code=201, description='Kweek has been liked successfully.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.expect(create_model('Kweek ID', {
                                        'id': fields.String(description='The id of the kweek to be liked.')
                                    }))
    def post(self):
        """
         Like a rekweek.
        """
        pass

    @kweeks_api.response(code=200, description='Kweek has been unliked successfully.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='str', description='The id of the kweek to be disliked', required=True)
    def delete(self):
        """
        Dislike a rekweek.
        """
        pass