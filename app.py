from flask import Flask
from flask_restplus import Api
from flask_socketio import SocketIO
from database_migration.migration import migrate_non_cli
import api_namespaces
import database_manager
import config
import patch

app = Flask(__name__)

authorizations = {
    'KwikkerKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'TOKEN'
    },
    'KwikkerCode': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'CODE'
    }
}
api = Api(app, authorizations=authorizations, doc='/api/doc', title='Kwikker API', version='1.0',
          validate=True)
socketio = SocketIO(app)
create_model = api.model
secret_key = None
code = None


def initialize_database():
    """
        Initializes the database. If the production configuration the database credentials are
        obtained from app.config (set in config.py). Else, the the database credentials of the
        developer are used.


        *Returns:*
            - *True*: If the database connection was successful.
            - *False*: Otherwise. The response of the database connection attempt is also printed.
    """
    db_name = app.config['DATABASE_NAME']
    db_username = app.config['DATABASE_USERNAME']
    db_password = app.config['DATABASE_PASSWORD']
    db_host = app.config['DATABASE_HOST']
    db_port = app.config['DATABASE_PORT']
    migrations_db_name = app.config['MIGRATIONS_DATABASE_NAME']

    if migrate_non_cli(_db_name=db_name,
                       _db_username=db_username,
                       _db_password=db_password,
                       _db_host=db_host,
                       _db_port=db_port,
                       _migrations_db_name=migrations_db_name,
                       _db_manager=database_manager.db_manager):
        response = database_manager.db_manager.initialize_connection(db_name=db_name,
                                                                     db_username=db_username,
                                                                     db_password=db_password,
                                                                     host=db_host,
                                                                     port=db_port)

        if response is None:
            print('Connected to the database successfully.')
            return True
        else:
            print('Could not connect to the database.')
            print(response)
            return False
    else:
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


def initialize(env):
    """
        Loads the app configuration from the config.py, registers the api namespaces,
        and initializes the database.

        *Parameters:*
            - *env (string)*: The environment in which the server is running for configurations

        *Returns:*
            - *True*: If the database connection was successful.
            - *False*: Otherwise. The response of the database connection attempt is also printed.
    """
    # Initializing configuration
    if env == 'production':
        app.config.from_object(config.ProductionConfig)
    elif env == 'production test':
        app.config.from_object(config.ProductionTestingConfig)
    elif env == 'development test':
        app.config.from_object(config.TestingConfig)
        app.config.from_pyfile('config_local.py')
    else:
        app.config.from_object(config.DevelopmentConfig)
        app.config.from_pyfile('config_local.py')

    global secret_key
    global code
    secret_key = app.config['SECRET_KEY']
    code = app.config['CODE_KEY']
    # Apply monkey patches
    patch.patch_flask_restplus_fields()
    api_namespaces.initialize_api_namespaces(api=api)
    import_routes()
    return initialize_database()


@app.after_request
def apply_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def run(env):
    """
            Attempts to initialize the app, and runs it if the initialization was successful.
    """
    if initialize(env):
        #socketio.run(app)
        socketio.run(app, host='0.0.0.0')
