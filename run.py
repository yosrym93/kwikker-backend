from app import app, api
from api_namespaces import APINamespaces
import users_profiles.routes
import users_interactions.routes
import authentication_and_registration.routes
import kweeks.routes
import timelines_and_trends.routes
import notifications.routes
import direct_messages.routes
import media.routes

if __name__ == '__main__':
    APINamespaces.initialize_api_namespaces(api=api)
    app.run(debug=True)
