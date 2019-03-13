from flask_restplus import Resource, fields
from app import create_model
from api_namespaces import APINamespaces

account_api = APINamespaces.account_api


@account_api.route('/login')
class Login(Resource):
    @account_api.response(code=200, description='Logged in successfully.', model=create_model('Token', model={
        'Token': fields.String(description='Access token.')
    }))
    @account_api.response(code=404,
                          description='A user with matching credentials does not exist.')
    @account_api.expect(create_model('User Credentials', {
                            'username': fields.String(description='The username of the user logging in.'),
                            'password': fields.String(description='The password of the user logging in.')
                        }))
    def post(self):
        """ Authenticates user and provide an access token for Kwikker. """
        pass


@account_api.route('/registration')
class Registration(Resource):
    @account_api.response(code=201, description='User registered successfully, email confirmation pending.')
    @account_api.response(code=403, description='Username or email already exists.',
                          model=create_model('Registration Failure', {
                            'username_already_exists': fields.Boolean,
                            'email_already_exists': fields.Boolean
                          }))
    @account_api.expect(create_model('User Credentials', {
        'username': fields.String(description='The username of the new user.'),
        'password': fields.String(description='The password of the new user.'),
        'email': fields.String(description='The email of the user new user.')
    }))
    def post(self):
        """ Register a new user. The user then is required to confirm their email address. """
        pass


@account_api.route('/registration/confirmation')
class RegistrationConfirmation(Resource):
    @account_api.expect(create_model('Confirmation Code', {
                                        'confirmation_code': fields.String('The confirmation code of the user.')
                                    }))
    @account_api.response(code=200, description='User confirmed.', model=create_model('Token', model={
        'Token': fields.String(description='Access token.')
    }))
    @account_api.response(code=404,
                          description='An unconfirmed user with the given confirmation code does not exist.')
    def post(self):
        """ Confirm a user's registration and provide an access token. """
        pass


@account_api.route('/registration/resend_email')
class RegistrationResendEmail(Resource):
    @account_api.expect(create_model('Email - Resend Confirmation Email', {
                            'email': fields.String('The email of the user pending email confirmation.')
                        }))
    @account_api.response(code=200, description='Email resent successfully.')
    @account_api.response(code=404, description='The user does not exist or is already confirmed.')
    def post(self):
        """ Resends an email to confirm the user registration. """
        pass


@account_api.route('/logout')
class Logout(Resource):
    @account_api.response(code=200, description='Logged out successfully.')
    def post(self):
        """ Logging a user out and expiring their access token """
        pass


@account_api.route('/forget_password')
class ForgetPassword(Resource):
    @account_api.expect(create_model('Email - Forget Password', {
        'email': fields.String('The email of the user requesting a password reset.')
    }))
    @account_api.response(code=200, description='A new password was sent successfully.')
    @account_api.response(code=404,
                          description='A user with the provided email does not exist.')
    def post(self):
        """ Resets the user's password and sends a new password by email. """
        pass