from app import app, api
from routes import initialize_routes


if __name__ == '__main__':
    initialize_routes(api)
    app.run(debug=True)

