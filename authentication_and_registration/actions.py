from . import query_factory
from functools import wraps
from flask import request
from flask_restplus import abort
import jwt
import datetime
from datetime import timedelta
from app import secret_key, app, code
from flask_mail import Mail, Message
from threading import Thread
import bcrypt
mail = Mail(app)
root = app.config['FRONT_END_ROOT']


def get_user_by_email(email):
    """
    search for user with the given email

    *Returns:*
        -the user.
    """
    return query_factory.get_user_by_email(email)


def get_user_by_username(username):
    """
    search for user with the given username

    *Returns:*
        -the user.
    """
    return query_factory.get_user_by_username(username)


def add_user(username, password, email):
    """
    Add user to the system

    When a user sign up for the first time this function hash the password given, then calls
    another function in the query factory to add the user

    *Parameters:*
        - *username(string)*: holds the value of the username.
        - *password(string)*: holds the value of the password.
        - *email(string)*: holds the value of the email.

    *Returns:*
       - two boolean values one indicates if the username already exists and the other indicates if the
         email already exists
    """
    username_bool = query_factory.username_exists(username)
    email_bool = query_factory.email_exists(email)
    print(username_bool, email_bool)
    if username_bool or email_bool:
        return username_bool, email_bool
    # Hash a password for the first time, with a randomly-generated salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query_factory.add_user(username, hashed.decode('utf-8'), email)
    return username_bool, email_bool


def async_send_email(msg):
    """
    Sending emails Asynchronous

    *Parameters:*
        - *message(object)*: holds the message to be send.
    """
    with app.app_context():
        mail.send(msg)


def send_email(email, username, password, subject, url, html, confirm):
    """
        Sending email

        *Parameters:*
             - *email(string)*: holds the value of the email.
             - *username(string)*: holds the value of the username.
             - *password(string)*: holds the value of the password.
             - *subject(string)*: holds the value of the subject of the email
             - *url(string)*: holds the value of the url attached to the email.
             - *html(string)*: holds the value of the html statements that will be sent.
             - *confirm(bool)*: true if the email is an confirmation mail, false if its a reset password mail.
    """
    msg = Message(subject, sender='no-reply@kwikker.me', recipients=[email])
    if confirm:
        codee = create_token(username, password, code)
    else:
        codee = create_token(username, password)
    link = root+url+codee.decode('utf-8')
    msg.html = html
    msg.html += '<a href="'+link+'">Click me</a>'
    thr = Thread(target=async_send_email, args=[msg])
    thr.start()


def verify(username, password):
    """
    verify user.

    investigate whether the user is on the system or not, by calling another function
    in the query factory that access the database.

    *Parameters:*
        - *username(string)*: holds the value of the username.
        - *password(string)*: holds the value of the password.

    *Returns:*
        -*True*: if the user is on the system.
        -*False*: if the user is not on the system.
    """
    return query_factory.is_user(username, password)


def confirm_user(username):
    """
        confirm user in the system with thee given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    query_factory.confirm_user(username)
    pass


def update_user_username(username, new_username):
    """
        update username of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_username(string)*:holds the value of the new username

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    if query_factory.username_exists(new_username):
        return False
    else:
        print('2')
        return query_factory.update_user_username(username, new_username)


def update_user_password(username, new_password):
    """
        update password of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_password(string)*:holds the value of the new password

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    print(hashed)
    print(new_password)
    return query_factory.update_user_password(username, hashed.decode('utf-8'))


def update_user_email(username, new_email):
    """
        update the email of the user with the given username.

        *Parameters:*
            -*username(string)*:holds the value of the username.
            -*new_email(string)*:holds the value of the new email

         *Returns:*
         -*True:* updated successfully.
         -*False:* error happened.
    """
    print(new_email)
    if query_factory.email_exists(new_email):
        return False
    else:
        return query_factory.update_user_email(username, new_email)


def create_token(username, password, secret=secret_key):
    """
    Generate token.

    Encode the payload (date of expiration, username) with the secret key.

    *Parameters:*
        -*username(string)*: holds the value of the username.
        -*password(string)*: holds the value of the password.

    *Returns:*
        -*Token*:the token created.
    """
    exp = datetime.datetime.utcnow()+timedelta(days=1)
    payload = {
        'username': username,
        'password': password,
        'exp': exp
    }
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token


def get_user(codee):
    user = None
    try:
        user = jwt.decode(codee, code, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        abort(401, message='Signature expired. try to resend the email.')

    except jwt.InvalidTokenError:
        abort(404, message='An unconfirmed user with the given confirmation code does not exist.')

    #    print('TOKEN: {}'.format(token))
    if not query_factory.username_exists(user['username']):
        abort(404, message='An unconfirmed user with the given confirmation code does not exist.')

    return user['username'], user['password']


def authorize(f):
    """
    Token verification Decorator.

    this decorator validate the token passed in the header with the endpoint.

    *Returns:*
        -*Error Response,401*: if the token is not given in the header, expired or invalid.
        -*Username*:if the token is valid it allows the access and return the username of the user.
    """
    @wraps(f)  # pragma:no cover
    def decorated(*args, **kwargs):

        token = None
        user = None
        if 'TOKEN' in request.headers:
            token = request.headers['TOKEN']

        if not token:
            abort(401, message='Token is missing.')

        try:
            user = jwt.decode(token, secret_key, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            abort(401, message='Signature expired. Please log in again.')

        except jwt.InvalidTokenError:
            abort(401, message='Invalid token. Please log in again.')

        # print('TOKEN: {}'.format(token))
        if not query_factory.username_exists(user['username']):
            abort(401, message='User not found.')
        return f(authorized_username=user['username'], *args, **kwargs)

    return decorated  # pragma:no cover
