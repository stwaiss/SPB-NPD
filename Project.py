from google.appengine.ext import ndb

class Project(ndb.Model):
    projectNumber = ndb.StringProperty(required=True)
    projectName = ndb.StringProperty(required=True)
    projectBrand = ndb.StringProperty(required=True)
    projectCategory = ndb.StringProperty(required=True)
    projectRegions = ndb.StringProperty(repeated=True)
    projectTypeNumber = ndb.IntegerProperty(required=True)
    isActive = ndb.BooleanProperty(required=True)
    createdBy = ndb.KeyProperty(required=True)
    projectManager = ndb.KeyProperty(required=True)
    gateID = ndb.IntegerProperty()
    dateCreated = ndb.DateTimeProperty(required=True)
    dateExitFactory = ndb.DateTimeProperty()
    gateArray = ndb.KeyProperty(repeated=True)