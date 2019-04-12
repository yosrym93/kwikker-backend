from flask_restplus import Resource, abort
from flask import request
from models import Kweek, Trend
import api_namespaces
from . import actions
from authentication_and_registration.actions import authorize

trends_api = api_namespaces.trends_api
search_api = api_namespaces.search_api
timelines_api = api_namespaces.timelines_api
kweeks_api = api_namespaces.kweeks_api


@timelines_api.route('/home')
class HomeTimeline(Resource):
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     " To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized access.')
    @timelines_api.response(code=404, description='Username or kweek id does not exist.')
    @timelines_api.response(code=500, description='An error occurred in the server.')
    @timelines_api.response(code=400, description='Invalid ID provided.')
    @timelines_api.marshal_with(Kweek.api_model, as_list=True)
    @timelines_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of kweeks in the home page of the authorized user. """
        last_retrieved_kweek_id = request.args.get('last_retrieved_kweek_id')
        try:
            kweeks = actions.get_home_kweeks(authorized_username=authorized_username,
                                             last_retrieved_kweek_id=last_retrieved_kweek_id)
            if kweeks is None:
                abort(404, message='A kweek with the provided ID does not exist.')
            return kweeks, 200
        except TypeError:
            abort(500, message='An error occurred in the server.')
        except ValueError:
            abort(400, 'Invalid ID provided.')


@timelines_api.route('/profile')
class ProfileTimeline(Resource):
    @timelines_api.param(name='username', type='str',
                         description="The username of the user whose profile kweeks are requested.")
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     "To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized access.')
    @timelines_api.response(code=404, description='Username or kweek id does not exist.')
    @timelines_api.response(code=500, description='An error occurred in the server.')
    @timelines_api.response(code=400, description='Invalid ID provided.')
    @timelines_api.marshal_with(Kweek.api_model, as_list=True)
    @timelines_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of kweeks in the profile of a user. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        else:
            required_username = request.args.get('username')
            last_retrieved_kweek_id = request.args.get('last_retrieved_kweek_id')
            if not actions.is_user(required_username):
                abort(404, message='A user with this username does not exist.')
            try:
                kweeks = actions.get_profile_kweeks(authorized_username=authorized_username,
                                                    required_username=required_username,
                                                    last_retrieved_kweek_id=last_retrieved_kweek_id)
                if kweeks is None:
                    abort(404, message='A kweek with the provided ID does not exist.')
                return kweeks, 200
            except TypeError:
                abort(500, message='An error occurred in the server.')
            except ValueError:
                abort(400, 'Invalid ID provided.')


@timelines_api.route('/mentions')
class MentionsTimeline(Resource):
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     "To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized access.')
    @timelines_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of kweeks where the authorized user is mentioned. """
        pass


@kweeks_api.route('/user/liked')
class UserLikedTweets(Resource):
    @kweeks_api.param(name='last_retrieved_kweek_id', type='str',
                      description="Nullable. Normally the request returns the first 20 kweeks when null."
                                  "To retrieve more send the id of the last kweek retrieved.")
    @kweeks_api.param(name='username', type='str', required=True,
                      description="The username of the user whose liked kweeks are requested.")
    @kweeks_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @timelines_api.response(code=404, description='Username or kweek id does not exist.')
    @timelines_api.response(code=500, description='An error occurred in the server.')
    @timelines_api.response(code=400, description='Invalid ID provided.')
    @timelines_api.marshal_with(Kweek.api_model, as_list=True)
    @kweeks_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of kweeks liked by a user. """
        if 'username' not in request.args.keys():
            abort(404, message='No username was sent.')
        else:
            required_username = request.args.get('username')
            last_retrieved_kweek_id = request.args.get('last_retrieved_kweek_id')
            if not actions.is_user(required_username):
                abort(404, message='A user with this username does not exist.')
            try:
                kweeks = actions.get_user_liked_kweeks(authorized_username=authorized_username,
                                                       required_username=required_username,
                                                       last_retrieved_kweek_id=last_retrieved_kweek_id)
                if kweeks is None:
                    abort(404, message='A kweek with the provided ID does not exist.')
                return kweeks, 200
            except TypeError:
                abort(500, message='An error occurred in the server.')
            except ValueError:
                abort(400, 'Invalid ID provided.')


@search_api.route('/kweeks')
class KweeksSearch(Resource):
    @search_api.param(name='search_text', type='str',
                      description='The text entered by the user in the search bar.', required=True)
    @search_api.param(name='last_retrieved_kweek_id', type='str',
                      description="Nullable. Normally the request returns the first 20 kweeks when null."
                                  "To retrieve more send the id of the last kweek retrieved.")
    @search_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @search_api.response(code=401, description='Unauthorized access.')
    @search_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """
            Retrieves a list of kweeks that matches (either fully or partially) the sent string.
            The order of the returned kweeks is based on the users who are followed by the authorized user.
        """
        pass


@trends_api.route('/')
class Trends(Resource):
    @trends_api.param(name='last_retrieved_trend_id', type='str',
                      description="Nullable. Normally the request returns the first 20 trends when null."
                                  "To retrieve more send the id of the last trend retrieved.")
    @trends_api.response(code=200, description='Trends returned successfully.', model=[Trend.api_model])
    @trends_api.response(code=401, description='Unauthorized access.')
    @trends_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of available trends. """
        pass


@trends_api.route('/kweeks')
class Trends(Resource):
    @trends_api.param(name='trend_id', type='str',
                      description='The id of the trend.', required=True)
    @trends_api.param(name='last_retrieved_kweek_id', type='str',
                      description="Nullable. Normally the request returns the first 20 kweeks when null."
                                  "To retrieve more send the id of the last kweek retrieved.")
    @trends_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @trends_api.response(code=401, description='Unauthorized access.')
    @trends_api.response(code=404, description='Trend does not exist.')
    @trends_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        """ Retrieves a list of kweeks in a given trend. """
        pass
