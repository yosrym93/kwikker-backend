from flask_restplus import Resource, fields
from app import create_model
from api_namespaces import APINamespaces

media_api = APINamespaces.media_api


@media_api.route('/')
class Media(Resource):
    @media_api.param(name='image_file', description='Image file.', type='file')
    @media_api.response(code=201, description='Image has been uploaded successfully',
                        model=create_model('Media ID',
                                           model={'media_id':
                                                  fields.String(description='The id of the uploaded image.')}))
    @media_api.response(code=404, description='Media not found. Uploading failed.')
    @media_api.response(code=401, description='Unauthorized access.')
    def post(self):
            """
            Post a new media file .
            """
            pass
