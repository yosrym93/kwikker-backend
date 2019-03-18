from . import query_factory
from functools import wraps
from flask import request
import jwt
import datetime
from datetime import timedelta
secret_key = 'kwikkerSecretKeyIsSALTS'


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


def create_token(username):
    """
    Generate token.

    Encode the payload (date of expiration, username) with the secret key.

    *Parameters:*
        -*username(string)*: holds the value of the username.

    *Returns:*
        -*Token*:the token created.
    """
    exp = datetime.datetime.utcnow()+timedelta(days=1)
    payload = {
        'username': username,
        'exp': exp
    }
    token = jwt.encode(payload, secret_key)
    return token


def authorize(f):
    """
    Token verification Decorator.

    this decorator validate the token passed in the header with the endpoint.

    *Returns:*
        -*Error Response,401*: if the token is not given in the header, expired or invalid.
        -*Username*:if the token is valid it allows the access and return the username of the user.
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        if 'TOKEN' in request.headers:
            token = request.headers['TOKEN']

        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            user = jwt.decode(token, secret_key)['username']

        except jwt.InvalidTokenError:
            return {'message': 'Invalid token. Please log in again.'}, 401

        except jwt.ExpiredSignatureError:
            return {'message': 'Signature expired. Please log in again.'}, 401

        print('TOKEN: {}'.format(token))
        print(user)
        return f(username=user, *args, **kwargs)

    return decorated
