from flask import Flask
from flask_restplus import Api
import api_namespaces


app = Flask(__name__)
api = Api(app, doc='/api/doc', title='Kwikker API', version='1.0')
create_model = api.model


def initialize_database():
    db_name = app.config['DATABASE_NAME']
    db_username = app.config['DATABASE_USERNAME']
    db_password = app.config['DATABASE_PASSWORD']
    """
    response = database_manager.db_manager.initialize_connection(db_name=db_name, db_username=db_username,
                                                                 db_password=db_password)
    """
    response = None     # Temporary, until the database is created
    if response is None:
        print('Connected to the database successfully.')
        return True
    else:
        print('Could not connect to the database.')
        print(response)
        return False


def import_routes():
    # These imports are only used to make the routes files load. Looking for a better fix.
    import users_profiles.routes
    import users_interactions.routes
    import authentication_and_registration.routes
    import kweeks.routes
    import timelines_and_trends.routes
    import notifications.routes
    import direct_messages.routes
    import media.routes


def initialize():
    app.config.from_object('config.DevelopmentConfig')
    api_namespaces.initialize_api_namespaces(api=api)
    import_routes()
    return initialize_database()


def run():
    if initialize():
        app.run()
