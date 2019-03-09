from app import api, create_model
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
    api_model = create_model('User', {
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
    api_model = create_model('User Profile', {
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
    api_model = create_model('Hashtag', {
        'id': fields.String(description='The unique id of the trend.'),
        'indices': fields.List(fields.Integer,
                               description='The indices of the beginning and ending of the hashtag in the kweek.')
    })

    def __init__(self, json):
        self.id = json['id']
        self.indices = (json['indices'][0], json['indices'][1])

    def to_json(self):
        return {
            'id': self.id,
            'indices': [self.indices[0], self.indices[1]]
        }


class Mention:
    api_model = create_model('Mention', {
        'username': fields.String(description='The username of the mentioned user.'),
        'indices': fields.List(fields.Integer,
                               description='The indices of the beginning and ending of the mention in the kweek.')
    })

    def __init__(self, json):
        self.username = json['username']
        self.indices = (json['indices'][0], json['indices'][1])

    def to_json(self):
        return {
            'username': self.username,
            'indices': [self.indices[0], self.indices[1]]
        }


class RekweekInfo:
    api_model = create_model('Rekweek Info', {
        'rekweeker_name': fields.String(description='The screen name of the user who rekweeked the kweek.'),
        'rekweeker_username': fields.String(description='The username of the user who rekweeked the kweek.')
    })

    def __init__(self, json):
        self.rekweeker_name = json['rekweeker_name']
        self.rekweeker_username = json['rekweeker_username']

    def to_json(self):
        return {
            'rekweeker_name': self.rekweeker_name,
            'rekweeker_username': self.rekweeker_username
        }


class Kweek:
    # TODO: Add a description for each parameter
    api_model = create_model('Kweek', {
        'id': fields.String(description='The id of the kweek.'),
        'created_at': fields.DateTime(description='The date and time when the kweek was created.'),
        'text': fields.String(description='The text of the kweek.'),
        'media_url': fields.String(description='Nullable. The url of the image attached with the kweek,'
                                               ' if any.'),
        'user': fields.Nested(User.api_model, description='The user who wrote the kweek.'),
        'mentions': fields.List(fields.Nested(Mention.api_model), description='The mentions in the kweek.'),
        'hashtags': fields.List(fields.Nested(Hashtag.api_model), description='The hashtags in the kweek.'),
        'number_of_likes': fields.Integer(description='The number of likes of the kweek.'),
        'number_of_rekweeks': fields.Integer(description='The number of rekweeks of the kweek.'),
        'number_of_replies': fields.Integer(description='The number of replies of the kweek.'),
        'reply_to': fields.String(description='Nullable. The id of the kweek that this kweek is a reply to,'
                                              ' if any.'),
        'rekweek_info': fields.Nested(RekweekInfo.api_model,
                                      description= 'Nullable. The information of who rekweeked this kweek,'
                                                   'if returned as a rekweek.'),
        'liked_by_user': fields.Boolean(description='Whether or not the user liked this kweek.'),
        'rekweeked_by_user': fields.Boolean(description='Whether or not the user rekweeked this kweek.')
    })

    def __init__(self, json):
        self.id = json['id']
        self.created_at = json['created_at']
        self.text = json['text']
        self.media_url = json['media_url']
        self.user = User(json['user'])

        self.hashtags = []
        for hashtag in json['hashtags']:
            self.hashtags.append(hashtag)

        self.mentions = []
        for mention in json['mentions']:
            self.mentions.append(mention)

        self.number_of_likes = json['number_of_likes']
        self.number_of_rekweeks = json['number_of_rekweeks']
        self.number_of_replies = json['number_of_replies']
        self.reply_to = json['reply_to']
        self.rekweek_info = RekweekInfo(json['rekweek_info'])
        pass

    def to_json(self):
        json = {}
        json['id'] = self.id
        json['created_at'] = self.created_at
        json['text'] = self.text
        json['media_url'] = self.media_url
        json['user'] = self.user.to_json()

        json['hashtags'] = []
        for hashtag in self.hashtags:
            json['hashtags'].append(hashtag.to_json())

        json['mentions'] = []
        for mention in self.mentions:
            json['mentions'].append(mention.to_json())

        json['number_of_likes'] = self.number_of_likes
        json['number_of_rekweeks'] = self.number_of_rekweeks
        json['number_of_replies'] = self.number_of_replies
        json['reply_to'] = self.reply_to
        json['rekweek_info'] = self.rekweek_info.to_json()
        return json


class Notification:
    api_model = create_model('Notification', {
        'id': fields.String(description='a unique string representing the notification'),
        'created_at': fields.DateTime(description='the utc datetime of the notification when created'),
        'type': fields.String(description='type of the notification [possible values:follow,rekweek,like,reply]'),
        'username': fields.String(description='username of the notification'),
        'screen_name': fields.String(description='handle that the user identifies themselves with'),
        'kweek_id': fields.String(description='a unique string representing the kweek id ', required=False)  # Nullable
    })

    def __init__(self, json):
        self.id = json['id']
        self.created_at = json['created_at']
        self.type = json['type']
        self.username = json['username']
        self.screen_names = json['screen_name']
        self.kweek_id = json['kweek_id']

    def to_json(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'type': self.type,
            'username': self.username,
            'screen_name': self.screen_names,
            'kweek_id': self.kweek_id
        }


class DirectMessage:
    api_model = create_model('Direct Message', {
        'created_at': fields.DateTime(description='the utc datetime of the message when created'),
        'text': fields.String(description='the content of the message'),
        'media_url': fields.String(description='the url pointing directly to the message', required=False)  # Nullable
    })

    def __init__(self, json):
        self.created_at = json['created_at']
        self.text = json['text']
        self.media_url = json['media_url']

    def to_json(self):
        return{
            'created_at': self.created_at,
            'text': self.text,
            'media_url': self.media_url
        }


class Conversation:
    api_model = create_model('Conversation', {
        'user': fields.Nested(User.api_model, description='the user information a.k.a mini-user information'),
        'last_message': fields.Nested(DirectMessage.api_model, description='last message information')
    })

    def __init__(self, json):
        self.user = json['user'],
        self.last_message = json['last_message']

    def to_json(self):
        return {
            'user': self.user,
            'last_message': self.last_message
        }


class Trend:
    api_model = create_model('Trend', {
        'id': fields.String(description='The id of the trend.'),
        'text': fields.String(description='The text of the trend.'),
        'number_of_kweeks': fields.Integer(description='The number of kweeks in the trend.')
    })

    def __init__(self, json):
        self.id = json['id'],
        self.text = json['text'],
        self.number_of_kweeks = json['number_of_kweeks']

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'number_of_kweeks': self.number_of_kweeks
        }
