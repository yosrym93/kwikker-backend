from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
api = Api(app, doc='/api/doc', title='Kwikker API', version='1.0')
create_model = api.model


