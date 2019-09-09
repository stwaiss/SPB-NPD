# Spectrum Brands New Product Development Management System:
# This software is designed to host a web application to help Spectrum Brands
# of Middleton, Wisconsin...
#
# This software is proprietary to Spectrum Brands and will not be distributed, altered, or
# otherwise used by parties not owned or overseen by Spectrum Brands
#
#  Copyright 2019 - Sean Tyler Waiss, Waiss & Co.


import webapp2
import jinja2
import os
import datetime
import csv
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
