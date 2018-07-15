import unittest
from scripts.base import *
from flask import Flask
from scripts.database import *
from scripts.users import *
from scripts.courses import *
from scripts.surveys import *
from scripts.responses import *

ADMIN = 3
STAFF = 2
STUDENT = 1
NONE = 0
# Added this to database.py
# def add_enrolment(self, username, course_id, course_semester):
#         session = self.session()
#         enrolment = Enrolment(username=username, course_id=course_id, course_semester=course_semester)
#         self.add_row(session, enrolment)

class StudentEnrolment(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        self.database.open('sqlite:///data/UnitTest.db')

    def tearDown(self):
        Base.metadata.drop_all()

    def testEnrolled(self):
        counter = 0

        self.database.add_user("harold" , "pass" , STUDENT)
        self.database.add_course("TEST1001" , "1s1")
        self.database.add_enrolment("harold" , "TEST1001" , "1s1")

        session = self.database.session()
        rowset = session.query(Enrolment).filter(User.username == "harold").all()
        for enrolment in rowset:
            self.assertEqual(enrolment.course_id, "TEST1001"), "user 'harold' is enrolled in the wrong course"
            counter = 1
        self.assertEqual(counter, 1), " user 'harold' not enrolled in anything, adding enrolment not working"
        session.close()

    def testNotEnrolled(self):
        counter = 0

        self.database.add_user("harold" , "pass" , STUDENT)
        self.database.add_course("TEST1001" , "1s1")

        session = self.database.session()
        rowset = session.query(Enrolment).filter(User.username == "harold").all()
        for enrolment in rowset:
            counter = 1
        self.assertNotEqual(counter, 1), "Non-existent enrolment found for user 'harold'"
        session.close()

    def testNonUserEnrolled(self):
        counter = 0

        session = self.database.session()
        rowset = session.query(Enrolment).filter(User.username == "harold").all()
        for enrolment in rowset:
            counter = 1
        self.assertNotEqual(counter, 1), "Non-existent user found to have enrolment"
        session.close()

if __name__ == '__main__':
    unittest.main()
