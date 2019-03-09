from flask_restplus import Namespace, Resource,fields
from app import create_model
from models import Kweek,User
kweeks_api = Namespace(name='Kweeks', path='/kweeks')
media_api = Namespace(name='Media', path='/media')

'''
    Use @kweeks_api and @media_api instead of api
    Replace the following class with your resources
'''

@kweeks_api.route('/')
class General_Kweeks(Resource):
    @kweeks_api.expect(Kweek.api_model)
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.response(code=200, description='Kweek created successfully')
    def post(self):
        """
        Create a new Kweek.
        """
        pass

    @kweeks_api.response(code=200, description='kweek has been deleted successfully')
    @kweeks_api.response(code=404, description='Kweek was not found')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='int', description=' Kweek id to be deleted',required=True)
    def delete(self):
        """
       Delete an existing Kweek.
        """
        pass

    @kweeks_api.response(code=200, description='Kweek has been returned successfully',
    model = create_model('TheWholeKweek', model={'Kweek': fields.Nested(Kweek.api_model,description='.'),'replies':fields.List(fields.Nested(Kweek.api_model,description='replies of a particular kweek'))}))
    @kweeks_api.response(code=404, description='Kweek was not found')
    @kweeks_api.param(name='id', type='int', description=' Id of the kweek to be retrieved',required=True)
    def get(self):
        """
       Retrieve a Kweek with its replies.
        """
        pass

@kweeks_api.route('/replies/')
class Relpies_Kweeks(Resource):
     @kweeks_api.response(code=200, description='replies have been returned successfully', model=create_model('Replies', model={'replies': fields.List(fields.Nested(Kweek.api_model,description='replies on a particular kweek'))}))
     @kweeks_api.param(name='reply_to', type='int',description='Id of the kweek of which the replies belongs to',required=True)
     def get(self):
         """
         Retrieve replies of a Kweek.
         """
         pass

@kweeks_api.route('/rekweek/')
class RekweekKweeks(Resource):
     @kweeks_api.param(name='id', type='string', description='Id of the rekweek to get rekweeked ',required=True)
     @kweeks_api.response(code=401, description='Unauthorized access.')
     @kweeks_api.response(code=200, description='Reweek created successfully')
     @kweeks_api.response(code=404, description='The Kweek is no more available')
     def put(self):
             """
             Create a new Rekweek.
             """
             pass

     @kweeks_api.response(code=200, description='Rekweek has been deleted successfully')
     @kweeks_api.response(code=404, description='Kweek was not found')
     @kweeks_api.response(code=401, description='Unauthorized access.')
     @kweeks_api.param(name='id', type='string', description='Id of the rekweek to be deleted',required=True)
     def delete(self):
         """
        Delete an existing rekweek.
         """
         pass

@kweeks_api.route('/rekweekers/')
class RekweekersKweeks(Resource):
     @kweeks_api.response(code=200, description='Rekweerkers have been returned successfully',
      model=create_model('Rekweekers', model={'rekweekers': fields.List(fields.Nested(User.api_model,description='List of the rekweekers to the kweek'))}))
     @kweeks_api.param(name='id', type='string', description='rekweek id of which its rekweekres are to be retrieved',required=True)
     def get(self):
        """
       Retrieve rekweekers of a rekweek.
        """
        pass

@kweeks_api.route('/likers')
class LikersKweeks(Resource):
    @kweeks_api.response(code=200, description='Likers have been returned successfully',
                         model=create_model('Likers', model={'Likers': fields.List(fields.Nested(User.api_model, description='List of the Likers of a kweek'))}))
    @kweeks_api.param(name='id', type='string', description='The kweek id to be liked',required=True)
    def get(self):
        """
       Retrieve likers of a rekweek .
        """
        pass

@kweeks_api.route('/like/')
class LikeKweeks(Resource):
    @kweeks_api.response(code=200, description='kweek has been liked successfully')
    @kweeks_api.response(code=404, description='kweek is not found')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='string', description='The id of the kweek to e liked',required=True)
    def put(self):
        """
         Like a rekweek.
        """
        pass

    @kweeks_api.response(code=404, description='kweek was not found')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    @kweeks_api.param(name='id', type='string', description='The id of the kweek to be dislike',required=True)
    def delete(self):
        """
        Dislike a rekweek.
        """
        pass

@media_api.route('/')
class GeneralMedia(Resource):
    @media_api.expect(create_model('file ', model={
    'file': fields.String (description=' the file format to be uploaded')}))
    @kweeks_api.response(code=200, description='file has been uploaded successfully',
                         model=create_model('file_id', model={ 'file_id': fields.String(description='The id of the uploaded file.')}))
    @kweeks_api.response(code=404, description='uploading failed')
    @kweeks_api.response(code=401, description='Unauthorized access.')
    def post(self):
            """
            Post a new media file .
            """
            pass

