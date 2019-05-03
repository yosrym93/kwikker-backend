from flask_restplus import Resource, fields, abort
from flask import request
from app import create_model
from models import Kweek, User, NullableString
from kweeks.actions import create_kweek, delete_kweek, get_kweek_with_replies, create_rekweek, delete_rekweek, \
    like_kweek, dislike_kweek, get_rekweekers, get_likers
import api_namespaces
from authentication_and_registration.actions import authorize

kweeks_api = api_namespaces.kweeks_api


@kweeks_api.route('/')
class Kweeks(Resource):
    @kweeks_api.expect(create_model('Created Kweek', {
        'text': fields.String,
        'reply_to': NullableString(description='The id of the kweek that this kweek '
                                               'is a reply to. Null if the kweek is not'
                                               ' a reply.'),
        'media_id': NullableString(description='Id of the media, provided when uploaded.')
    }), validate=True)
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid ID to be replied to')
    @kweeks_api.response(code=404, description='The kweek to be replied to does not exist.')
    @kweeks_api.response(code=400, description='No text body found.')
    @kweeks_api.response(code=200, description='Kweek has been created successfully.')
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """
        Create a new Kweek or reply.
        """
        check, message, code = create_kweek(request.get_json(), authorized_username)
        if check:
            return 'Kweek has been created successfully.', code
        else:
            abort(code, message)

    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Deletion is not allowed.')
    @kweeks_api.response(code=200, description='Kweek has been created successfully.')
    @kweeks_api.param(name='id', type='str', description='The id of the Kweek to be deleted.', required=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """
        Delete an existing Kweek.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, code = delete_kweek(request.args.get('id'), authorized_username)
        if check:
            return 'Kweek has been deleted successfully.', code
        else:
            abort(code, message)

    @kweeks_api.response(code=200, description='Kweek has been returned successfully.',
                         model=create_model('Kweek & Replies',
                                            model={'Kweek': fields.Nested(Kweek.api_model,
                                                                          description='The returned Kweek.'),
                                                   'replies': fields.List(fields.Nested(Kweek.api_model,
                                                                                        description='Direct replies '
                                                                                                    'of the Kweek'))}))
    @kweeks_api.marshal_with(create_model('Kweek & Replies',
                                          model={'kweek': fields.Nested(Kweek.api_model,
                                                                        description='The returned Kweek.'),
                                                 'replies': fields.List(fields.Nested(Kweek.api_model,
                                                                                      description='Direct replies '
                                                                                                  'of the Kweek'))}))
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='id', type='str', description='Id of the Kweek to be retrieved', required=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
        Retrieve a Kweek with its replies.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, kweek_obj, replies_obj_list, code = \
            get_kweek_with_replies(request.args.get('id'), authorized_username, False)
        if check:
            return {
                'kweek': kweek_obj,
                'replies': replies_obj_list
            }
        else:
            abort(code, message)


@kweeks_api.route('/kweek_only')
class KweekOnly(Resource):
    @kweeks_api.response(code=200, description='kweek has been returned successfully.',
                         model=Kweek.api_model)
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='id', type='str', description='Id of the Kweek to be retrieved', required=True)
    @kweeks_api.marshal_with(Kweek.api_model, as_list=False)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
        Retrieve the kweek without its replies.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, kweek_obj, replies_obj_list, code = \
            get_kweek_with_replies(request.args.get('id'), authorized_username, False)
        if check:
            return kweek_obj, 200
        else:
            abort(code, message)


@kweeks_api.route('/replies')
class KweekReplies(Resource):
    @kweeks_api.response(code=200, description='Replies have been returned successfully.',
                         model=[Kweek.api_model])
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='reply_to', type='str',
                      description='Id of the Kweek that the replies belong to.', required=True)
    @kweeks_api.marshal_with(Kweek.api_model, as_list=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
        Retrieve replies of a Kweek.
        """
        if not request.args.get('reply_to'):
            abort(400, 'please provide the kweek id')
        check, message, kweek_obj, replies_obj_list, code = \
            get_kweek_with_replies(request.args.get('reply_to'), authorized_username, True)
        if check:
            return replies_obj_list, 200
        else:
            abort(code, message)


@kweeks_api.route('/rekweek')
class Rekweek(Resource):
    @kweeks_api.expect(create_model('Kweek ID', {
        'id': fields.String(description='The id of the kweek to be rekweeked.')
    }), validate=True)
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=200, description='Rekweek has been created successfully.')
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """
        Create a new Rekweek.
        """
        check, message, code = create_rekweek(request.get_json(), authorized_username)
        if check:
            return 'Rekweek has been created successfully.', 200
        else:
            abort(code, message)

    @kweeks_api.response(code=200, description='Rekweek has been deleted successfully.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Deletion is not allowed.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='string', description='Id of the rekweek to be deleted', required=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """
        Delete an existing rekweek.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, code = delete_rekweek(request.args.get('id'), authorized_username)
        if check:
            return 'Rekweek has been deleted successfully.', 200
        else:
            abort(code, message)


@kweeks_api.route('/like')
class Like(Resource):
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=200, description='Like has been created successfully.')
    @kweeks_api.expect(create_model('Kweek ID', {
        'id': fields.String(description='The id of the kweek to be liked.')
    }), validate=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """
         Like a rekweek.
        """
        check, message, code = like_kweek(request.get_json(), authorized_username)
        if check:
            return 'Like has been created successfully.', 200
        else:
            abort(code, message)

    @kweeks_api.response(code=200, description='Like has been deleted successfully.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.response(code=401, description='Deletion is not allowed.')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='str', description='The id of the kweek to be disliked', required=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def delete(self, authorized_username):
        """
        Dislike a kweek.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, code = dislike_kweek(request.args.get('id'), authorized_username)
        if check:
            return 'Like has been deleted successfully.', 200
        else:
            abort(code, message)


@kweeks_api.route('/rekweekers')
class KweekRekweekers(Resource):
    @kweeks_api.response(code=200, description='Rekweerkers have been returned successfully.',
                         model=[User.api_model])
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='id', type='str',
                      description='Id of the Kweek whose rekweekers are to be retrieved', required=True)
    @kweeks_api.marshal_with(User.api_model, as_list=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
        Retrieve rekweekers of a kweek.
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, users_obj_list, code = get_rekweekers(request.args.get('id'), authorized_username)
        if check:
            return users_obj_list, 200
        else:
            abort(code, message)


@kweeks_api.route('/likers')
class KweekLikers(Resource):
    @kweeks_api.response(code=200, description='Likers have been returned successfully.',
                         model=[User.api_model])
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=400, description='Invalid kweek ID.')
    @kweeks_api.response(code=404, description='Kweek does not exist.')
    @kweeks_api.param(name='id', type='string', description='The kweek id to get its likers', required=True)
    @kweeks_api.marshal_with(User.api_model, as_list=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
        Retrieve likers of a kweek .
        """
        if not request.args.get('id'):
            abort(400, 'please provide the kweek id')
        check, message, users_obj_list, code = get_likers(request.args.get('id'), authorized_username)
        if check:
            return users_obj_list, 200
        else:
            abort(code, message)
