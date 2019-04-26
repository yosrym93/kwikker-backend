from app import create_model
from flask_restplus import fields


# ------------ API Models ------------ #
"""
    Each model includes:
        - an 'api_model' for flask_restplus documentation
        - a constructor to build it from a dictionary (flask_restplus converts json objects to python dictionaries)
        - a 'to_json' function to serialize it (returns it in the form of a python dictionary)
"""


class User:
    api_model = create_model('User', {
        'username': fields.String(description='The user name.'),
        'screen_name': fields.String(description='The name shown on profile screen.'),
        'profile_image_url': fields.String(description='Url for profile image.'),
        'following': fields.Boolean(description='Nullable. Does the authorized user follow this user? '
                                                'Null if the authorized user is the same as the user in the query.'),
        'follows_you': fields.Boolean(description='Nullable. Does this user follow the authorized user? '
                                                  'Null if the authorized user is the same as the user in the query.'),
        'blocked': fields.Boolean(description='Nullable. Is this user blocked by the authorized user? '
                                              'Null if the authorized user is the same as the user in the query.'),
        'muted': fields.Boolean(description='Nullable. Is this user muted by the authorized user? '
                                            'Null if the authorized user is the same as the user in the query.')
    })

    def __init__(self, json):
        self.username = json["username"]
        self.screen_name = json["screen_name"]
        self.profile_image_url = json["profile_image_url"]
        self.following = json["following"]
        self.follows_you = json["follows_you"]
        self.blocked = json["blocked"]
        self.muted = json["muted"]

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

    def __repr__(self):
        return "<Test username:%s screen_name:%s profile_image_url:%s following:%s follows_you:%s" \
               " blocked:%s muted:%s   >" % \
               (self.username, self.screen_name, self.profile_image_url, self.following, self.follows_you,
                self.blocked, self.muted)


class UserProfile:
    api_model = create_model('User Profile', {
        'username': fields.String(description='The user name.'),
        'screen_name': fields.String(description='The name shown on profile screen.'),
        'bio': fields.String(description='The biography of the user'),
        'birth_date': fields.Date(description='The birth date of the user'),
        'created_at': fields.DateTime(description='Time created at'),
        'followers_count': fields.Integer(description='Integer indicates number of people follow you.'),
        'following_count': fields.Integer(description='Integer indicates number of people you follow.'),
        'kweeks_count': fields.Integer(description='Integer indicates number of tweets which called kweeks.'),
        'likes_count': fields.Integer(description='Integer indicates number of likes.'),
        'profile_banner_url': fields.String(description='Url for profile banner which is cover photo.'),
        'profile_image_url': fields.String(description='Url for profile image.'),
        'following': fields.Boolean(description='Nullable. Does the authorized user follow this user? '
                                                'Null if the authorized user is the same as the user in the query.'),
        'follows_you': fields.Boolean(description='Nullable. Does this user follow the authorized user? '
                                                  'Null if the authorized user is the same as the user in the query.'),
        'blocked': fields.Boolean(description='Nullable. Is this user blocked by the authorized user? '
                                              'Null if the authorized user is the same as the user in the query.'),
        'muted': fields.Boolean(description='Nullable. Is this user muted by the authorized user? '
                                            'Null if the authorized user is the same as the user in the query.')
    })

    def __init__(self, json):
        self.username = json["username"]
        self.screen_name = json["screen_name"]
        self.bio = json["bio"]
        self.birth_date = json["birth_date"]
        self.created_at = json["created_at"]
        self.followers_count = json["followers_count"]
        self.following_count = json["following_count"]
        self.kweeks_count = json["kweeks_count"]
        self.likes_count = json["likes_count"]
        self.profile_banner_url = json["profile_banner_url"]
        self.profile_image_url = json["profile_image_url"]
        self.following = json["following"]
        self.follows_you = json["follows_you"]
        self.blocked = json["blocked"]
        self.muted = json["muted"]

    def to_json(self):
        return {
            'username': self.username,
            'screen_name': self.screen_name,
            'bio': self.bio,
            'birth_date': self.birth_date,
            'created_at': self.created_at,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'kweeks_count': self.kweeks_count,
            'likes_count': self.likes_count,
            'profile_banner_url': self.profile_banner_url,
            'profile_image_url': self.profile_image_url,

            'following': self.following,
            'follows_you': self.follows_you,
            'blocked': self.blocked,
            'muted': self.muted
        }


class Hashtag:
    api_model = create_model('Hashtag', {
        'id': fields.String(description='The unique id of the trend.'),
        'indices': fields.List(fields.Integer,
                               description='The indices of the beginning and ending of the hashtag in the kweek.'),
        'text': fields.String(description='The body of the hashtag.')
    })

    def __init__(self, json):
        self.id = json['id']
        self.indices = (json['indices'][0], json['indices'][1])
        self.text = (json['text'])

    def __repr__(self):
        return "<id:%s indices:%s text:%s >" % \
               (self.id, self.indices, self.text)

    def to_json(self):
        return {
            'id': self.id,
            'indices': [self.indices[0], self.indices[1]],
            'text': self.text
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

    def __repr__(self):
        return "<username:%s indices:%s  >" % \
               (self.username, self.indices)

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

    def __repr__(self):
        return "<rekweeker_name:%s rekweeker_username:%s  >" % \
               (self.rekweeker_name, self.rekweeker_username)

    def to_json(self):
        return {
            'rekweeker_name': self.rekweeker_name,
            'rekweeker_username': self.rekweeker_username
        }


class Kweek:
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
        'rekweek_info': fields.Nested(RekweekInfo.api_model, allow_null=True,
                                      description='Nullable. The information of who rekweeked this kweek,'
                                                  'if returned as a rekweek.'),
        'liked_by_user': fields.Boolean(description='Whether or not the user liked this kweek.'),
        'rekweeked_by_user': fields.Boolean(description='Whether or not the user rekweeked this kweek.')
    })

    def __init__(self, json):
        self.id = json['id']
        self.created_at = json['created_at']
        self.text = json['text']
        self.media_url = json['media_url']
        self.user = json['user']
        self.hashtags = json['hashtags']
        self.mentions = json['mentions']
        self.number_of_likes = json['number_of_likes']
        self.number_of_rekweeks = json['number_of_rekweeks']
        self.number_of_replies = json['number_of_replies']
        self.reply_to = json['reply_to']
        self.liked_by_user = json['liked_by_user']
        self.rekweeked_by_user = json['rekweeked_by_user']
        self.rekweek_info = (json['rekweek_info'])

    def __repr__(self):
        return "<Test id:%s created_at:%s text:%s media_url:%s user:%s" \
               " hashtags:%s mentions:%s number_of_likes:%s number_of_rekweeks:%s number_of_replies:%s" \
               " reply_to:%s rekweek_info:%s   >" % \
               (self.id, self.created_at, self.text, self.media_url, self.user, self.hashtags,
                self.mentions, self.number_of_likes, self.number_of_rekweeks, self.number_of_replies,
                self.reply_to, self.rekweek_info)

    def to_json(self):
        json = {'id': self.id, 'created_at': self.created_at, 'text': self.text, 'media_url': self.media_url,
                'user': self.user.to_json(), 'hashtags': []}
        for hashtag in self.hashtags:
            json['hashtags'].append(hashtag.to_json())
        json['mentions'] = []
        for mention in self.mentions:
            json['mentions'].append(mention.to_json())
        json['number_of_likes'] = self.number_of_likes
        json['number_of_rekweeks'] = self.number_of_rekweeks
        json['number_of_replies'] = self.number_of_replies
        json['reply_to'] = self.reply_to
        if self.rekweek_info is not None:
            json['rekweek_info'] = self.rekweek_info.to_json()
        else:
            json['rekweek_info'] = None
        json['liked_by_user'] = self.liked_by_user
        json['rekweeked_by_user'] = self.rekweeked_by_user
        return json


class Notification:
    api_model = create_model('Notification', {
        'id': fields.String(description='A unique string representing the notification.'),
        'created_at': fields.String(description='The utc datetime of the notification when created.'),
        'type': fields.String(description='Type of the notification [possible values:follow,rekweek,like,reply, '
                                          'mentions].'),
        'username': fields.String(description='Username of the notification.'),  # involved_username
        'screen_name': fields.String(description='Handle that the user identifies themselves with.'),
        'kweek_id': fields.String(description='Nullable,a unique string representing the kweek id.',
                                  nullable=True),  # Nullable
        'kweek_text': fields.String(description='The text of the kweek.'),
        'profile_pic_url': fields.String(description='The profile picture URL of the involved person who liked,'
                                                     'followed,etc).')
    })

    def __init__(self, json):
        self.id = json['id']
        self.created_at = json['created_at']
        self.type = json['type']
        self.username = json['username']
        self.screen_name = json['screen_name']
        self.kweek_id = json['kweek_id']
        self.kweek_text = json['kweek_text']
        self.profile_pic_url = json['profile_pic_url']

    def to_json(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'type': self.type,
            'username': self.username,
            'screen_name': self.screen_name,
            'kweek_id': self.kweek_id,
            'kweek_text': self.kweek_text,
            'profile_pic_url': self.profile_pic_url
        }


class DirectMessage:
    api_model = create_model('Direct Message', {
        'id': fields.String(description='A unique string representing the message.'),
        'from_username': fields.String(description='username who sent the message.'),
        'to_username': fields.String(description='username who wants to receive that message.'),
        'created_at': fields.String(description='The utc datetime of the message when created.'),
        'text': fields.String(description='The content of the message.'),
        'media_url': fields.String(description='Nullable. The url of the media.',
                                   nullable=True)  # Nullable
    })

    def __init__(self, json):
        self.id = json['id']
        self.from_username = json['from_username']
        self.to_username = json['to_username']
        self.created_at = json['created_at']
        self.text = json['text']
        self.media_url = json['media_url']

    def to_json(self):
        return{
            'id': self.id,
            'from_username': self.from_username,
            'to_username': self.to_username,
            'created_at': self.created_at,
            'text': self.text,
            'media_url': self.media_url
        }


class Conversation:
    api_model = create_model('Conversation', {
        'user': fields.Nested(User.api_model, description='The user information a.k.a mini-user information.'),
        'last_message': fields.Nested(DirectMessage.api_model, description='Last message information.')
    })

    def __init__(self, json):
        self.user = json['user'],
        self.last_message = json['last_message']

    def to_json(self):
        return {
            'user': self.user[0],
            'last_message': self.last_message
        }


class Trend:
    api_model = create_model('Trend', {
        'id': fields.String(description='The id of the trend.'),
        'text': fields.String(description='The text of the trend.'),
        'number_of_kweeks': fields.Integer(description='The number of kweeks in the trend.')
    })

    def __init__(self, json):
        self.id = json['id']
        self.text = json['text']
        self.number_of_kweeks = json['number_of_kweeks']

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'number_of_kweeks': self.number_of_kweeks
        }


# Use this in @api.expect() instead of fields.String for any string that accepts null value
class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'
