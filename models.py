from app import api
from flask_restplus import fields


# ------------ API Models ------------ #
"""
    Each model includes:
        - an 'api_model' for flask_restplus documentation
        - a constructor to build it from a dictionary (flask_restplus converts json objects to python dictionaries)
        - a 'to_json' function to serialize it (returns it in the form of a python dictionary)
"""


class User:
    # TODO: Add a description for each parameter
    api_model = api.model('User', {
        'username': fields.String,
        'screen_name': fields.String,
        'profile_image_url': fields.String,
        'following': fields.Boolean,
        'follows_you': fields.Boolean,
        'blocked': fields.Boolean,
        'muted': fields.Boolean
    })

    def __init__(self, json):
        # TODO: replace None with the values from the dictionary
        self.username = None
        self.screen_name = None
        self.profile_image_url = None
        self.following = None
        self.follows_you = None
        self.blocked = None
        self.muted = None

    def to_json(self):
        return {
            'username': self.username,
            'screen_name': self.screen_name,
            'profile_image_url': self.profile_image_url,
            'following': self.following,
            'follows_you': self.follows_you,
            'blocked': self.blocked,
            'muted': self.muted
        }


class UserProfile:
    # TODO: Add a description for each parameter
    api_model = api.model('User Profile', {
        'username': fields.String(),
        'screen_name': fields.String,
        'bio': fields.String,
        'created_at': fields.DateTime,
        'followers_count': fields.Integer,
        'following_count': fields.Integer,
        'kweeks_count': fields.Integer,
        'likes_count': fields.Integer,
        'profile_banner_url': fields.String,
        'profile_image_url': fields.String,
        'following': fields.Boolean,
        'follows_you': fields.Boolean,
        'blocked': fields.Boolean,
        'muted': fields.Boolean
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class Hashtag:
    # TODO: Add a description for each parameter
    api_model = api.model('Hashtag', {
        'id': fields.String,
        'indices': fields.List(fields.Integer)
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class Mention:
    # TODO: Add a description for each parameter
    api_model = api.model('Mention', {
        'username': fields.String,
        'indices': fields.List(fields.Integer)
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class RekweekInfo:
    # TODO: Add a description for each parameter
    api_model = api.model('Rekweek Info', {
        'rekweeker_name': fields.String,
        'rekweeker_username': fields.String
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class Kweek:
    # TODO: Add a description for each parameter
    api_model = api.model('Kweek', {
        'id': fields.String,
        'created_at': fields.DateTime,
        'text': fields.String,
        'imageUrl': fields.String,  # Nullable
        'user': fields.Nested(User.api_model),
        'hashtags': fields.List(fields.Nested(Hashtag.api_model)),
        'mentions': fields.List(fields.Nested(Mention.api_model)),
        'number_of_likes': fields.Integer,
        'number_of_rekweeks': fields.Integer,
        'number_of_replies': fields.Integer,
        'reply_to': fields.String,   # Nullable, kweek id
        'rekweek_info': fields.Nested(RekweekInfo.api_model)  # Nullable
    })

    def __init__(self, json):
        # TODO: implement
        # Use the nested objects constructors to build them
        pass

    def to_json(self):
        # TODO: implement
        # Use the nested objects to_json function to convert them
        pass


class Notification:
    # TODO: Add a description for each parameter
    api_model = api.model('Notification', {
        'id': fields.String,
        'created_at': fields.DateTime,
        'type': fields.String,  # Possible values: 'follow', 'rekweek', 'like', 'reply' # TODO: search for another type
        'username': fields.String,
        'screen_name': fields.String,
        'kweek_id': fields.String   # Nullable
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class DirectMessage:
    # TODO: Add a description for each parameter
    api_model = api.model('Direct Message', {
        'created_at': fields.DateTime,
        'text': fields.String,
        'media_url': fields.String  # Nullable
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass


class Conversation:
    # TODO: Add a description for each parameter
    api_model = api.model('Conversation', {
        'user': fields.Nested(User.api_model),
        'last_message': fields.Nested(DirectMessage.api_model)
    })

    def __init__(self, json):
        # TODO: implement
        pass

    def to_json(self):
        # TODO: implement
        pass
