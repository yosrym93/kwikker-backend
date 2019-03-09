from flask_restplus import Namespace, Resource, fields
from app import create_model
account_api = Namespace(name='Account', path='/account')


@account_api.route('/login')
class Login(Resource):
    @account_api.param(name='username', type='str', required=True,
                       description="The username of the user who is going to login.")
    @account_api.param(name='password', type='str', required=True,
                       description="The password of the user who is going to login.")
    @account_api.response(code=200, description='Logged in successfully.', model=create_model('Token', model={
        'Token': fields.String(description='Value which represents the token.')
    }))
    @account_api.response(code=404,
                          description='The account requested is invalid,such as a username or password does not exist.')
    def post(self):
        """ Confirm username and password, Assign a token to the user in order to use Kwikker. """
        pass


@account_api.route('/registration')
class Registration(Resource):
    @account_api.param(name='username', type='str', required=True,
                       description="The username of the user who is going to login.")
    @account_api.param(name='password', type='str', required=True,
                       description="The password of the user who is going to login.")
    @account_api.param(name='email', type='str', required=True,
                       description="The email of the user who is going to login.")
    @account_api.response(code=201, description='Registered in successfully, user has been '
                                                'created successfully to the system only confirmation missing.')
    def post(self):
        """ Adding new user to Kwikker, Confirmation is needed. """
        pass


@account_api.route('/registration/confirmation')
class RegistrationConfirmation(Resource):
    @account_api.param(name='code', type='str', required=True,
                       description='The code of the user.')
    @account_api.response(code=201, description='Registration is confirmed.', model=create_model('Token', model={
        'Token': fields.String(description='Value which represents the token.')
    }))
    @account_api.response(code=404,
                          description='The account requested is invalid,such as a username or password does not exist')
    def post(self):
        """ User has been confirmed,return a token. """
        pass


@account_api.route('/registration/resend_email')
class RegistrationResendEmail(Resource):
    @account_api.param(name='email', type='str', required=True,
                       description="The email of the user who is going to confirm his registration.")
    @account_api.response(code=200, description='Resend successfully.')
    @account_api.response(code=404, description='The email not found.')
    def post(self):
        """ Resends an email to confirm the user registration. """
        pass


@account_api.route('/logout')
class Logout(Resource):
    @account_api.response(code=200, description='Logged out successfully.')
    def post(self):
        """ Logging out the user, delete token. """
        pass


@account_api.route('/forget_password')
class ForgetPassword(Resource):
    @account_api.param(name='email', type='str', required=True,
                       description='Email of the user, in order to change his password.')
    @account_api.response(code=200, description='A new password sent successfully.')
    @account_api.response(code=404,
                          description='Email not found, the email is not on the system.')
    def post(self):
        """ Sending an email containing the new password. """
        pass
