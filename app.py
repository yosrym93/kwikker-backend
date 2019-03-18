from flask import Flask
from flask_restplus import Api
import api_namespaces
import database_manager


app = Flask(__name__)
authorizations = {
    'KwikkerKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'TOKEN'
    }
}
api = Api(app, authorizations=authorizations, doc='/api/doc', title='Kwikker API', version='1.0')
create_model = api.model


def initialize_database():
    """
        Initializes the database. If the production configuration the database credentials are
        obtained from app.config (set in config.py). Else, the the database credentials of the
        developer are used.


        *Returns:*
            - *True*: If the database connection was successful.
            - *False*: Otherwise. The response of the database connection attempt is also printed.
    """
    if app.config['ENV'] == 'production':
        db_name = app.config['DATABASE_NAME']
        db_username = app.config['DATABASE_USERNAME']
        db_password = app.config['DATABASE_PASSWORD']
    else:
        # Replace with your local database credentials
        db_name = 'kwikker'
        db_username = 'postgres'


        db_password = '8949649'

    response = database_manager.db_manager.initialize_connection(db_name=db_name, db_username=db_username,
                                                                 db_password=db_password)

    if response is None:
        print('Connected to the database successfully.')
        return True
    else:
        print('Could not connect to the database.')
        print(response)
        return False


def import_routes():
    """
        Dummy function to import the modules containing the routes (endpoints) so that the api
        documentation is generated on startup.
    """

    import users_profiles.routes
    import users_interactions.routes
    import authentication_and_registration.routes
    import kweeks.routes
    import timelines_and_trends.routes
    import notifications.routes
    import direct_messages.routes
    import media.routes


def initialize():
    """
        Loads the app configuration from the config.py, registers the api namespaces,
        and initializes the database.


        *Returns:*
            - *True*: If the database connection was successful.
            - *False*: Otherwise. The response of the database connection attempt is also printed.
    """
    app.config.from_object('config.DevelopmentConfig')
    api_namespaces.initialize_api_namespaces(api=api)
    import_routes()
    return initialize_database()


def run():
    """
            Attempts to initialize the app, and runs it if the initialization was successful.
    """
    if initialize():
        app.run()
