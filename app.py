from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, doc='/api/doc')
app.config['RESTPLUS_MASK_SWAGGER'] = False



