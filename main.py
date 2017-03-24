import os
import webapp2
import jinja2
import json
import time
import logging

from google.appengine.ext import ndb
from google.appengine.api import mail

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                              autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class IndexPageHandler(BaseHandler):
    def get(self):
        self.render('index.html')

class LoginPageHandler(BaseHandler):
    def get(self):
        self.render('login.html')

app = webapp2.WSGIApplication([
    ('/', IndexPageHandler),
    ('/login', LoginPageHandler),
    ], debug=True)
