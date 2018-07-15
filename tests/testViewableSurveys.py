import unittest
from flask import Flask
from scripts.base import *
from scripts.database import *
from scripts.users import *
from scripts.courses import *
from scripts.surveys import *
from scripts.responses import *

REVIEW = 0
OPEN = 1
CLOSED = 2

class testSurveysOnDash(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        self.database.open('sqlite:///UnitTest.db')
        
    def tearDown(self): 
        Base.metadata.drop_all()

    def testNormalViewSurvey(self):
        counter = 0

        q_id = self.database.add_question("Q_TITLE" , 2, [123, "1"])
        self.database.add_course("TEST1001" , "1s1")
        survey_id = self.database.add_survey("S_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])
        user_id = self.database.add_user("harold" , "pass" , STUDENT)
        self.database.add_enrolment("harold" , "TEST1001" , "1s1")
        self.database.change_survey_status(self.database.get_surveys(survey_id), OPEN)

        session = self.database.session()
        rowset = self.database.get_viewable(user_id, OPEN)
        for survey in rowset:
            self.assertEqual(survey.title, "S_TITLE") , "Wrong survey will be viewable on user 'harold''s dashboard"
            counter = 1
        self.assertEqual(counter, 1), "survey for a course in which student is enrolled and has not already been filled out will not appear on dashboard"
        session.close()

    def testNoViewSurvey(self):
        counter = 0

        q_id = self.database.add_question("Q_TITLE" , 2, [123, "1"])
        self.database.add_course("TEST1001" , "1s1")
        survey_id = self.database.add_survey("S_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])
        user_id = self.database.add_user("harold" , "pass" , STUDENT)
        self.database.change_survey_status(self.database.get_surveys(survey_id), OPEN)

        session = self.database.session()
        rowset = self.database.get_viewable(user_id, OPEN)
        for survey in rowset:
            counter = 1
        self.assertEqual(counter, 0), "survey viewable on student's dash despite not bein enrolled in the course that it is affiliated with"
        session.close()

    def testStaffReviewSurvey(self):
        counter = 0

        q_id = self.database.add_question("Q_TITLE" , 2, [123, "1"])
        course_id = self.database.add_course("TEST1001" , "1s1")
        survey_id = self.database.add_survey("S_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])
        user_id = self.database.add_user("harold" , "pass" , STAFF)
        self.database.add_enrolment("harold" , "TEST1001" , "1s1")
        

        session = self.database.session()
        rowset = self.database.get_viewable(user_id, REVIEW)
        for survey in rowset:
            self.assertEqual(survey.title, "S_TITLE") , "Wrong survey will be viewable on user 'harold''s dashboard"
            counter = 1
        self.assertEqual(counter, 1), "survey for a course in which student is enrolled and has not already been filled out will not appear on dashboard"
        session.close()


    def testStudentReviewSurvey(self):
        counter = 0
        
        q_id = self.database.add_question("Q_TITLE" , 2, [123, "1"])
        self.database.add_course("TEST1001" , "1s1")
        survey_id = self.database.add_survey("S_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])
        user_id = self.database.add_user("harold" , "pass" , STUDENT)

        session = self.database.session()
        rowset = self.database.get_viewable(user_id, OPEN)
        for survey in rowset:
            counter = 1
        self.assertEqual(counter, 0), "survey viewable on student's dash despite not being reviewed yet"
        session.close()


if __name__ == '__main__':
    unittest.main()