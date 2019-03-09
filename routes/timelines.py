from flask_restplus import Namespace, Resource
from .kweeks import kweeks_api
from models import Kweek, Trend

trends_api = Namespace(name='Trends', path='/trends')
search_api = Namespace(name='Search', path='/search')
timelines_api = Namespace(name='Timelines', path='/kweeks/timelines')


@timelines_api.route('/home')
class HomeTimeline(Resource):
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     "To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    def get(self):
        """ Retrieves a list of kweeks in the home page of the authorized user. """
        pass


@timelines_api.route('/profile')
class ProfileTimeline(Resource):
    @timelines_api.param(name='username', type='str', required=True,
                         description="The username of the user whose profile kweeks are requested.")
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     "To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    @timelines_api.response(code=404, description='User does not exist.')
    def get(self):
        """ Retrieves a list of kweeks in the profile of a user. """
        pass


@timelines_api.route('/mentions')
class MentionsTimeline(Resource):
    @timelines_api.param(name='last_retrieved_kweek_id', type='str',
                         description="Nullable. Normally the request returns the first 20 kweeks when null."
                                     "To retrieve more send the id of the last kweek retrieved.")
    @timelines_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @timelines_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    def get(self):
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
    @kweeks_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    @kweeks_api.response(code=404, description='User does not exist.')
    def get(self):
        """ Retrieves a list of kweeks liked by a user. """
        pass


@search_api.route('/kweeks')
class KweeksSearch(Resource):
    @search_api.param(name='search_text', type='str',
                      description='The text entered by the user in the search bar.', required=True)
    @search_api.param(name='last_retrieved_kweek_id', type='str',
                      description="Nullable. Normally the request returns the first 20 kweeks when null."
                                  "To retrieve more send the id of the last kweek retrieved.")
    @search_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @search_api.response(code=401, description='Unauthorized.')
    def get(self):
        """
            Retrieves a list of kweeks that matches (either fully or partially) the sent string.
            The order of the returned kweeks is based on the users who are followed by the authorized user.
        """
        pass


@trends_api.route('/')
class Trends(Resource):
    @search_api.param(name='last_retrieved_trend_id', type='str',
                      description="Nullable. Normally the request returns the first 20 trends when null."
                                  "To retrieve more send the id of the last trend retrieved.")
    @trends_api.response(code=200, description='Trends returned successfully.', model=[Trend.api_model])
    @trends_api.response(code=401, description='Unauthorized[User does not have enough privilege].')
    def get(self):
        """ Retrieves a list of available trends. """
        pass


@trends_api.route('/kweeks')
class Trends(Resource):
    @search_api.param(name='trend_id', type='str',
                      description='The id of the trend.', required=True)
    @search_api.param(name='last_retrieved_kweek_id', type='str',
                      description="Nullable. Normally the request returns the first 20 kweeks when null."
                                  "To retrieve more send the id of the last kweek retrieved.")
    @trends_api.response(code=200, description='Kweeks returned successfully.', model=[Kweek.api_model])
    @trends_api.response(code=401, description='Unauthorized.')
    @trends_api.response(code=404, description='Trend does not exist.')
    def get(self):
        """ Retrieves a list of kweeks in a given trend. """
        pass
