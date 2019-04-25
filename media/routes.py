from flask_restplus import Resource, fields, abort
from flask import request, send_from_directory
from app import create_model
from .import actions
import api_namespaces
from authentication_and_registration.actions import authorize
import os
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_api = api_namespaces.media_api


@media_api.route('/')
class Media(Resource):
    @media_api.param(name='image_file', description='Image file.', type='file')
    @media_api.response(code=201, description='Image has been uploaded successfully',
                        model=create_model('Media ID',
                                           model={'media_id':
                                                  fields.String(description='The id of the uploaded image.')}))
    @media_api.response(code=404, description='Media not found. Uploading failed.')
    @media_api.response(code=401, description='Unauthorized access.')
    @media_api.response(code=400, description='Not allowed extensions.')
    @media_api.param(name='file', description='image file.', required=True, type='file')
    @media_api.doc(security='KwikkerKey')
    @authorize
    def post(self,authorized_username):
        """
        Post a new media file. and return id of the file without extension
        """
        if 'file' not in request.files:
            return abort(404, message='No image file')
        file = request.files['file']
        response = actions.save_file(file)
        if response == 'No selected file':
            return abort(404, message=response)
        if response == 'not allowed extensions':
            return abort(400, message=response)
        return {"filename":response}, 200



@media_api.route('/get/<filename>',doc=False)
class get_Media (Resource):
    @staticmethod
    def get(filename):
        """ this endpoint gets the image given the url """
        try:
            filename =actions.get_extension_file(filename)
            os.chdir(os.path.dirname(APP_ROOT))
            return send_from_directory('images/media', filename)
        except Exception as E:
            if str(E) == "file is not found":
                abort(404, message='file is not found.')
