import unittest
from flask import Flask, session, redirect, url_for, render_template, flash
from functools import wraps
from scripts.database import *
from scripts import authentication
from scripts.routes import *

ADMIN = 3
STAFF = 2
STUDENT = 1
NONE = 0

database.open('sqlite:///data/survey_database.db')

class ValidStaffLogin(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.validStaffLogin = authentication.login("50", "staff670")

    def testLoginSuccess(self):
        assert self.validStaffLogin != False, "Users correct login details failed login"

    def testUsernameRetrieval(self):
        assert self.validStaffLogin.username == "50" , "correct username for user not being passed from login"

    def testPermissionsRetrieval(self):
        assert self.validStaffLogin.permissions == STAFF , "correct permission for user not being passed from login"

class InvalidLogin(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.validStaffLogin = authentication.login("12", "password")

    def testLoginSuccess(self):
        assert self.validStaffLogin == False, "Users incorrect login details succeeded in logging in"

class NoLogin(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.validStaffLogin = authentication.login("", "")

    def testLoginSuccess(self):
        assert self.validStaffLogin == False, "No login details succeeded in logging in"


if __name__ == "__main__":
    unittest.main() # run all tests
