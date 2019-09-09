from google.appengine.ext import ndb

class Employee(ndb.Model):
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    isAdmin = ndb.BooleanProperty(required=True)
    isActive = ndb.BooleanProperty(required=True)