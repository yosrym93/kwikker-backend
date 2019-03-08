from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, doc='/api/doc', title='Kwikker API')
create_model = api.model
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'


