from google.appengine.ext import ndb


class Gate(ndb.Model):
    projectKey = ndb.KeyProperty(required=True)
    gateID = ndb.IntegerProperty()
    dateCreated = ndb.DateTimeProperty(required=True)
    dateExpectedCompleted = ndb.DateTimeProperty()
    dateActualCompleted = ndb.DateTimeProperty()