from flask_restplus import Namespace


class APINamespaces:
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

    # Registers the api namespaces
    @staticmethod
    def initialize_api_namespaces(api):
        api.add_namespace(APINamespaces.timelines_api)
        api.add_namespace(APINamespaces.account_api)
        api.add_namespace(APINamespaces.kweeks_api)
        api.add_namespace(APINamespaces.user_api)
        api.add_namespace(APINamespaces.interactions_api)
        api.add_namespace(APINamespaces.trends_api)
        api.add_namespace(APINamespaces.messages_api)
        api.add_namespace(APINamespaces.notifications_api)
        api.add_namespace(APINamespaces.search_api)
        api.add_namespace(APINamespaces.media_api)
