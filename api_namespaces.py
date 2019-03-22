from flask_restplus import Namespace


user_api = Namespace(name='User', path='/user', description='Account settings and user profiles.')
interactions_api = Namespace(name='Interactions', path='/interactions',
                             description='Following, muting, and blocking')
account_api = Namespace(name='Account', path='/account', description='Login, logout and registration.')
kweeks_api = Namespace(name='Kweeks', path='/kweeks',
                       description='Interacting with kweeks.')
media_api = Namespace(name='Media', path='/media', description='Upload images to be used in kweeks and messages.')
trends_api = Namespace(name='Trends', path='/trends', description='Trends and related kweeks.')
search_api = Namespace(name='Search', path='/search', description='Search for kweeks or users.')
timelines_api = Namespace(name='Timelines', path='/kweeks/timelines',
                          description='Kweeks timelines.')
messages_api = Namespace(name='Direct Messages', path='/direct_message',
                         description='Direct messages and conversations.')
notifications_api = Namespace(name='Notifications', path='/notifications', description='User notifications.')


def initialize_api_namespaces(api):
    """
        Registers the api namespaces to the api object.
    """
    api.add_namespace(timelines_api)
    api.add_namespace(account_api)
    api.add_namespace(kweeks_api)
    api.add_namespace(user_api)
    api.add_namespace(interactions_api)
    api.add_namespace(trends_api)
    api.add_namespace(messages_api)
    api.add_namespace(notifications_api)
    api.add_namespace(search_api)
    api.add_namespace(media_api)
