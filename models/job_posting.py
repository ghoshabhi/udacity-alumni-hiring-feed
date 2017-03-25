from google.appengine.ext import ndb
from user import User

class JobPosting(ndb.Model):
    job_title = ndb.StringProperty()
    company = ndb.StringProperty()
    location = ndb.StringProperty()
    job_url = ndb.StringProperty(required=True)
    posted_by = ndb.KeyProperty(kind=User)
    attrs = ndb.StringProperty(repeated=True)
    # skills = ndb.StringProperty(repeated=True)
    # created = ndb.DateTimeProperty(auto_now_add=True)
    # experience = ndb.IntegerProperty(default=0)
    # is_internship = ndb.BooleanProperty(default=False)
    # is_remote = ndb.BooleanProperty(default=False)
