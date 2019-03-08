from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, doc='/api/doc',version='1.0')
app.config['RESTPLUS_MASK_SWAGGER'] = False



