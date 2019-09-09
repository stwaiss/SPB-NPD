from google.appengine.ext import ndb

class Project(ndb.Model):
    gateID = ndb.IntegerProperty()
    dateCreated = ndb.DateTimeProperty(required=True)
    dateExpectedCompletion = ndb.DateTimeProperty()
    dateActualCompletion = ndb.DateTimeProperty()
    gateArray = ndb.KeyProperty(repeated=True)