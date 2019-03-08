from .login_registration import account_api
from .kweeks import kweeks_api, media_api
from .users import user_api, interactions_api
from .messages_notifications import messages_api, notifications_api
from .timelines import search_api, trends_api
from .example import example_api


def initialize_routes(api):
    api.add_namespace(account_api)
    api.add_namespace(kweeks_api)
    api.add_namespace(user_api)
    api.add_namespace(interactions_api)
    api.add_namespace(trends_api)
    api.add_namespace(messages_api)
    api.add_namespace(notifications_api)
    api.add_namespace(search_api)
    api.add_namespace(media_api)
    api.add_namespace(example_api)
