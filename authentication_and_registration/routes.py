from flask_restplus import Resource, fields, abort
from flask import request
from app import create_model
import api_namespaces
from authentication_and_registration.actions import authorize
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
            token = actions.create_token(data['username'], data['password'])
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
        'email': fields.String(description='The email of the new user.'),
        'screen_name': fields.String(description='The screen name of the new user.'),
        'birth_date': fields.String(description='The birthdate of the new user.')
    }), validate=True)
    def post(self):
        """ Register a new user. The user then is required to confirm their email address. """
        data = request.get_json()
        user_exist, email_exist = actions.add_user(data['username'], data['password'], data['email'])
        # gelesh fn.
        if not (user_exist or email_exist):
            html = '<p>Confirming your account will give you </p> <b>full access to Kwikker</b>'
            subject = 'Confirm your Kwikker account, '+data['screen_name']
            # (email, username, password, subject, url, html, confirm)
            actions.send_email(data['email'], data['username'], data['password'], subject,
                               '/confirm/', html, True)
            return 201
        else:
            return {'username_already_exists': user_exist, 'email_already_exists': email_exist}, 403
        pass


@account_api.route('/registration/confirmation')
class RegistrationConfirmation(Resource):
    @account_api.expect(create_model('Confirmation Code', {
                                        'confirmation_code': fields.String('The confirmation code of the user.')
                                    }), validate=True)
    @account_api.response(code=200, description='User confirmed.', model=create_model('Token', model={
        'Token': fields.String(description='Access token.')
    }))
    @account_api.response(code=404,
                          description='An unconfirmed user with the given confirmation code does not exist.')
    def post(self):
        """ Confirm a user's registration and provide an access token. """
        data = request.get_json()
        username, password = actions.get_user(data['confirmation_code'])
        actions.confirm_user(username)
        token = actions.create_token(username, password)
        token = token.decode('utf-8')
        return {'token': token}, 200
        pass


@account_api.route('/registration/resend_email')
class RegistrationResendEmail(Resource):
    @account_api.expect(create_model('Email - Resend Confirmation Email', {
                            'email': fields.String('The email of the user pending email confirmation.')
                        }), validate=True)
    @account_api.response(code=200, description='Email resent successfully.')
    @account_api.response(code=404, description='The user does not exist or is already confirmed.')
    def post(self):
        """ Re-sends an email to confirm the user registration. """
        data = request.get_json()
        user = actions.get_user_by_email(data['email'])
        html = '<p>Confirming your account will give you </p> <b>full access to Kwikker</b>'
        subject = 'Confirm your Kwikker account, ' + data['username']
        actions.send_email(data['email'], user['username'], user['password'], subject,
                           '/confirm/', html, True)
        return 201
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
        """ Sends email to the user which give him access to change the password. """
        data = request.get_json()
        user = actions.get_user_by_email(data['email'])
        html = '<p>To reset your account </p>'
        subject = 'Request for changing password, ' + data['username']
        actions.send_email(data['email'], user['username'], user['password'], subject,
                           '/reset_password/', html, False)
        pass


@account_api.route('/update_profile/change_username')
class UpdateUsername(Resource):
    @account_api.expect(create_model('Username update data', {
        'username': fields.String(description='The new username.'),
        'password': fields.String(description='The old password.')
    }), validate=True)
    @account_api.response(code=200, description='Updated Successfully.', model=create_model('token', model={
        'token': fields.String(description='Access token.')
    }))
    @account_api.response(code=404, description='Username already exists')
    @account_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Updates the user's username. """
        data = request.get_json()
        is_updated = actions.update_user_username(authorized_username, data['username'])
        if is_updated:
            token = actions.create_token(data['username'], data['password'])
            token = token.decode('utf-8')
            return{'token': token}, 200
        else:
            abort(404, message='Username already exists')
        pass


@account_api.route('/update_profile/change_password')
class UpdatePassword(Resource):
    @account_api.expect(create_model('Password update data', {
        'password': fields.String(description='The new username.'),
    }), validate=True)
    @account_api.response(code=200, description='Updated Successfully.', model=create_model('token', model={
        'token': fields.String(description='Access token.')
    }))
    @account_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Updates the user's password. """
        data = request.get_json()
        print('1'*10)
        print(data['password'])
        is_updated = actions.update_user_password(authorized_username, data['password'])
        if is_updated:
            token = actions.create_token(authorized_username, data['password'])
            token = token.decode('utf-8')
            return{'token': token}, 200
        else:
            abort(404)
        pass


@account_api.route('/update_profile/change_email')
class UpdateEmail(Resource):
    @account_api.expect(create_model('Email update data', {
        'email': fields.String(description='The new username.'),
    }), validate=True)
    @account_api.response(code=200, description='Updated Successfully.')
    @account_api.response(code=404, description='Email already exists.')
    @account_api.doc(security='KwikkerKey')
    @authorize
    def post(self, authorized_username):
        """ Updates the user's email."""
        data = request.get_json()
        print('1')
        is_updated = actions.update_user_email(authorized_username, data['email'])
        if is_updated:
            return 200
        else:
            abort(404, message='Email already exists.')
        pass


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

    def get(self):
        print('before sending email')
        # (email, username, password, subject, url, html, confirm)
        html = '<p>Confirming your account will give you </p> <b>full access to Kwikker</b>'
        subject = 'Confirm your Kwikker account, Amr!'
        actions.send_email('amr.ahmed.abdelbaqi@gmail.com', 'username', 'acm', subject, 'kwikker.me/registration/confirmation', html, True)
        print('after sending email')
        pass