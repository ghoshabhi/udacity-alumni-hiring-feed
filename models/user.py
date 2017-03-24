from google.appengine.ext import ndb

default_avatar_url = "http://issues.freepbx.org/secure/useravatar?size=small&avatarId=12220"

class User(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    avatar_url = ndb.StringProperty(default=default_avatar_url)
    is_admin = ndb.BooleanProperty(default=False)
    is_hiring = ndb.BooleanProperty(default=False)
    is_searching = ndb.BooleanProperty(default=True)
