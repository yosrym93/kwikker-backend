from flask_restplus import Resource, fields, abort
from flask import request
from app import create_model
import api_namespaces
# from authentication_and_registration.actions import authorize
from . import actions
account_api = api_namespaces.account_api


@account_api.route('/login')
class Login(Resource):
    @account_api.response(code=200, description='Logged in successfully.', model=create_model('token', model={
        'token': fields.String(description='Access token.')
    }))
    @account_api.response(code=404,
                          description='A user with matching credentials does not exist.')
    @account_api.expect(create_model('User Credentials', {
                            'username': fields.String(description='The username of the user logging in.'),
                            'password': fields.String(description='The password of the user logging in.')
                        }), validate=True)
    def post(self):
        """ Authenticates user and provide an access token for Kwikker. """
        data = request.get_json()
        is_verified = actions.verify(data['username'], data['password'])
        if not is_verified:
            abort(404, message='A user with matching credentials does not exist.')
        else:
            token = actions.create_token(data['username'])
            token = token.decode('utf-8')
            return{'token': token}, 200
        pass


@account_api.route('/registration')
class Registration(Resource):
    @account_api.response(code=201, description='User registered successfully, email confirmation pending.')
    @account_api.response(code=403, description='Username or email already exists.',
                          model=create_model('Registration Failure', {
                            'username_already_exists': fields.Boolean,
                            'email_already_exists': fields.Boolean
                          }))
    @account_api.expect(create_model('User Registration Data', {
        'username': fields.String(description='The username of the new user.'),
        'password': fields.String(description='The password of the new user.'),
        'email': fields.String(description='The email of the user new user.')
    }), validate=True)
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
        """ Re-sends an email to confirm the user registration. """
        pass


@account_api.route('/forget_password')
class ForgetPassword(Resource):
    @account_api.expect(create_model('Email - Forget Password', {
        'email': fields.String('The email of the user requesting a password reset.')
    }), validate=True)
    @account_api.response(code=200, description='A new password was sent successfully.')
    @account_api.response(code=404,
                          description='A user with the provided email does not exist.')
    def post(self):
        """ Resets the user's password and sends a new password by email. """
        pass


'''
@account_api.route('/test')
class ExampleTest(Resource):
    @account_api.response(code=401, description='Signature expired. Please log in again.')
    @account_api.response(code=401, description='Invalid token. Please log in again.')
    @account_api.response(code=401, description='Token is missing.')
    @account_api.doc(security='KwikkerKey')
    # decorator that will verify the token sent
    @authorize
    def post(self, authorized_username):
        print('username:', authorized_username)
        return {'username': authorized_username}, 200

    @account_api.doc(security='KwikkerKey')
    @authorize
    def get(self, authorized_username):
        pass
'''