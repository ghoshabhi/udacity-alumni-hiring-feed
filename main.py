import os
import webapp2
import jinja2
import json
import time
import logging

from google.appengine.ext import ndb
from google.appengine.api import mail

from models import User, JobPosting
from utility import *

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

    def read_secure_cookie(self, name="user_id"):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
    	user_id = self.read_secure_cookie()
    	self.user = user_id and User.get_by_id(int(user_id))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

class IndexPageHandler(BaseHandler):
    def get(self):
        self.render('index.html', user = self.user)

class SignupPageHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password = self.request.get('password')
        verify_pass = self.request.get('verify_pass')
        is_hiring = self.request.get('is_hiring')
        location = self.request.get('location')

        if_user_exists = User.query(User.email == email).get()
        if if_user_exists:
            error = "Email Already exists!"
            return self.render("signup.html", error=error)
        if password != verify_pass:
            error="Passwords don't match!"
            return self.render("signup.html", error=error)
        if is_hiring:
            is_hiring=True
        else:
            is_hiring=False
        new_user_obj = User(
                first_name=first_name,
                last_name=last_name,
                location=location,
                email=email,
                pw_hash=hash_str(password),
                is_hiring=is_hiring
        )
        new_user_obj.put()
        full_name = new_user_obj.first_name + " " + new_user_obj.last_name
        self.render('login.html', new_user=full_name)

class LoginPageHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        email = self.request.get('email')
        pw = self.request.get('password')

        user = User.query(ndb.AND(\
                    User.email == email, User.pw_hash == hash_str(pw))).get()

        if user:
            self.response.headers.add_header(
                'Set-Cookie', 'user_id=%s, Expires=%s; Path=/'% \
                    (make_secure_val(str(user.key.id())), str(7*24*3600))\
            )
            time.sleep(0.1)
            return self.redirect('/')
        else:
            error="Username and/or Password don't match!"
            return self.render('login.html', error=error)


class LogoutHandler(BaseHandler):
    def get(self):
        self.logout()
        return self.redirect('/')

class PostJobHandler(BaseHandler):
    def get(self):
        self.render('post-job.html', user=self.user)

    def post(self):
        job_posting = self.request.get('job_posting')

        job_posting = job_posting.split("|")

        len_of_input = len(job_posting)

        if len_of_input == 1:
            new_job = JobPosting(company=job_posting[0])
            new_job.put()
            time.sleep(0.1)
            return self.redirect('/')

        if len_of_input == 2:
            new_job = JobPosting(company=job_posting[0], job_title=job_posting[1])
            new_job.put()
            time.sleep(0.1)
            return self.redirect('/')

        if len_of_input == 3:
            new_job = JobPosting(
                company=job_posting[0],
                job_title=job_posting[1],
                location=job_posting[2]
            )
            new_job.put()
            time.sleep(0.1)
            return self.redirect('/')

        if len_of_input == 4:
            new_job = JobPosting(
                company=job_posting[0],
                job_title=job_posting[1],
                location=job_posting[2],
                job_url=job_posting[3]
            )
            new_job.put()
            time.sleep(0.1)
            return self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', IndexPageHandler),
    ('/login', LoginPageHandler),
    ('/signup', SignupPageHandler),
    ('/logout', LogoutHandler),
    ('/post-job', PostJobHandler),
    ], debug=True)
