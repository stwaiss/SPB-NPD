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
from google.appengine.ext import ndb
from Employee import Employee


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # check if any employee is in the system, if not, create an administrator
        users = Employee.query().fetch()
        if len(users) == 0:
            swaiss = Employee(username="swaiss", password="swaiss", email="sean.waiss@spectrumbrands.com", isAdmin=True, isActive=True)
            swaiss.put()

            dummy = Employee(username="dummy", password="password", email="sean.waiss@spectrumbrands.com", isAdmin=False, isActive=True)
            dummy.put()

        # pulls current year to put into footer for copyrights
        dateTimeNow = datetime.datetime.now()
        curYear = dateTimeNow.year

        values = {
            "curYear": curYear
        }
        template = JINJA_ENVIRONMENT.get_template('HTML/Login.html')
        self.response.write(template.render(values))


class LoginHandler(webapp2.RequestHandler):
    def post(self):
        # pull form data
        postedUsername = self.request.get("username")
        postedPassword = self.request.get("password")

        # query all employees for a match
        matchingUser = Employee.query(Employee.username == postedUsername, Employee.password == postedPassword,
                                      Employee.isActive == True).fetch()

        # if match exists, set browser cookie
        if len(matchingUser) == 1:
            self.response.set_cookie("name", postedUsername, path='/')

            if matchingUser[0].isAdmin == True:
                # if user password is not set, direct to change password
                if matchingUser[0].password == "password":
                    self.redirect('/changePassword')
                    return
                self.redirect("/home")
                return
            else:
                # if user password is not set, direct to change password
                if matchingUser[0].password == "password":
                    self.redirect('/changePassword')
                    return
                self.redirect("/home")
                return

        # if match does not exist, return to log-in screen
        else:
            # else, redirect to log in screen with error
            dateTimeNow = datetime.datetime.now()
            curYear = dateTimeNow.year
            values = {
                'badCombo': 1,
                "curYear": curYear
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Login.html')
            self.response.write(template.render(values))
            return


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        # pull value from cookie key
        name = self.request.cookies.get('name')

        # delete cookie
        self.response.delete_cookie('name')

        # render successful log out template
        value = {
            'username': name
        }

        template = JINJA_ENVIRONMENT.get_template('HTML/Logout.html')
        self.response.write(template.render(value))


class ChangePasswordHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.cookies.get("name")
        users = Employee.query(Employee.username == name).fetch()

        # if cookie is correct, render page
        if len(users) != 0:
            curUser = users[0]

            # determine HTML template to use
            if curUser.isAdmin:
                isAdmin = 1
            else:
                isAdmin = 0

            # display form
            values = {
                "isAdmin": isAdmin,
                "username": name,
                "oldIncorrect": 0,
                "newDontMatch": 0
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/ChangePassword.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return

    def post(self):
        name = self.request.cookies.get("name")
        users = Employee.query(Employee.username == name).fetch()

        # if cookie is correct, render page
        if len(users) != 0:
            curUser = users[0]

            # determine HTML template to use
            if curUser.isAdmin:
                isAdmin = 1
            else:
                isAdmin = 0

            # pull form data
            postedCurPassword = self.request.get("curPassword")
            postedNewPassword = self.request.get("newPassword")
            postedRetypedNewPassword = self.request.get("retypedNewPassword")

            # compare posted password with actual password, if not match, throw error
            if postedCurPassword != curUser.password:
                values = {
                    "isAdmin": isAdmin,
                    "username": name,
                    "oldIncorrect": 1,
                    "newDontMatch": 0
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/ChangePassword.html')
                self.response.write(template.render(values))
                return

            # compare posted new and retyped passwords, if not match, throw error
            if postedNewPassword != postedRetypedNewPassword:
                values = {
                    "isAdmin": isAdmin,
                    "username": name,
                    "oldIncorrect": 0,
                    "newDontMatch": 1
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/ChangePassword.html')
                self.response.write(template.render(values))
                return

            # if old password matches what was in system, and the two new passwords match,
            # set user password to new password and give success message
            curUser.password = postedNewPassword
            curUser.put()

            values = {
                "isAdmin": isAdmin,
                "username": name
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/ChangePasswordSuccess.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return


class HomeHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        employees = Employee.query(Employee.username == name).fetch()

        # if cookie is correct, render page
        if len(employees) != 0:

            values = {
                'username': name,
                'employeeUsername': name,
                'e': employees[0]
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Home.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return


class ProjectHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        employees = Employee.query(Employee.username == name).fetch()

        # if cookie is correct, render page
        if len(employees) != 0:

            values = {
                'username': name,
                'employeeUsername': name,
                'e': employees[0]
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Projects.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return

class AdminManageEmployeeHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        admins = Employee.query(Employee.username == name, Employee.isAdmin == True).fetch()

        # if cookie is correct, render page
        if len(admins) != 0:
            employees = Employee.query().order(Employee.username).fetch()

            values = {
                "username": name,
                "employee": employees,
                "reset": 0,
                "employeeUsername": ""
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployees.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return


class AdminManageEmployeeCreateHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        admins = Employee.query(Employee.username == name, Employee.isAdmin == True).fetch()

        # if cookie is correct, render page
        if len(admins) != 0:
            values = {
                "username": name,
                "alreadyExists": 0,
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployeesCreate.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        admins = Employee.query(Employee.username == name, Employee.isAdmin == True).fetch()

        # if cookie is correct, render page
        if len(admins) != 0:
            # pull form data
            postedUsername = self.request.get('username')
            postedPassword = self.request.get('password')
            postedEmail = self.request.get('email')
            postedIsAdminList = self.request.get('admin')

            if postedIsAdminList != "":
                postedIsAdminBool = True
            else:
                postedIsAdminBool = False

            # check if username already exists, if yes, throw error
            matchingUsernames = Employee.query(Employee.username == postedUsername).fetch()

            if len(matchingUsernames) != 0:
                values = {
                    "username": name,
                    "alreadyExists": 1,
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployeesCreate.html')
                self.response.write(template.render(values))
                return

            # create employee and add to datastore
            newEmployee = Employee(username=postedUsername, password=postedPassword, email=postedEmail, isAdmin=postedIsAdminBool, isActive=True)
            newEmployee.put()

            values = {
                "username": name,
                "employee": newEmployee
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployeesCreateSuccess.html')
            self.response.write(template.render(values))

        else:
            self.redirect('/')
            return


class AdminManageEmployeeActivateHandler(webapp2.RequestHandler):
    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        admins = Employee.query(Employee.username == name, Employee.isAdmin == True).fetch()

        # if cookie is correct, render page
        if len(admins) != 0:
            # get employee key from page and turn back into employee entity
            employee_key_string = self.request.get('employee_key')
            employee_key = ndb.Key(urlsafe=employee_key_string)
            employee = employee_key.get()

            # if is true, set false, vice versa
            if employee.isActive:
                employee.isActive = False

            elif not employee.isActive:
                employee.isActive = True

            employee.put()

            employees = Employee.query().order(Employee.username).fetch()

            values = {
                "username": name,
                "employee": employees
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployees.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return


class AdminManageEmployeeResetHandler(webapp2.RequestHandler):
    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        admins = Employee.query(Employee.username == name, Employee.isAdmin == True).fetch()

        # if cookie is correct, render page
        if len(admins) != 0:
            # get employee key from page and turn back into employee entity
            employee_key_string = self.request.get('employee_key')
            employee_key = ndb.Key(urlsafe=employee_key_string)
            employee = employee_key.get()

            # reset password
            employee.password = "password"
            employee.put()

            # pull list for table
            employees = Employee.query().order(Employee.isAdmin, Employee.username).fetch()

            values = {
                "username": name,
                "employee": employees,
                "reset": 1,
                "employeeUsername": employee.username
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/AdminManageEmployees.html')
            self.response.write(template.render(values))
        else:
            self.redirect('/')
            return



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/changePassword', ChangePasswordHandler),
    ('/home', HomeHandler),
    ('/projects', ProjectHandler),
    ('/admin/manageEmployee', AdminManageEmployeeHandler),
    ('/admin/manageEmployee/create', AdminManageEmployeeCreateHandler),
    ('/admin/manageEmployee/activate', AdminManageEmployeeActivateHandler),
    ('/admin/manageEmployee/reset', AdminManageEmployeeResetHandler)
], debug=True)
