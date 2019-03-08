from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, doc='/api/doc')
create_model = api.model
app.config['RESTPLUS_MASK_SWAGGER'] = False



