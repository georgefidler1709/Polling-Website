import unittest
from base import *
from flask import Flask
from database import *
from users import *
from courses import *
from surveys import *
from responses import *

CHOICE = 0
TEXT = 1


class testSurvey(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        self.database.open('sqlite:///UnitTest.db')

    def tearDown(self):
        Base.metadata.drop_all()

    def testNormalSurvey(self):
        counter = 0

        q_id = self.database.add_question("Q_TITLE" , 1, [123, "1"])
        self.database.add_course("TEST1001" , "1s1")
        self.database.add_survey("S_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])

        session = self.database.session()
        rowset = session.query(Survey).filter(Survey.title == "S_TITLE").all()
        for survey in rowset:
            self.assertEqual(survey.title, "S_TITLE"), "Survey of incorrect title found. Survey creation insecure."
            counter = 1
        self.assertEqual(counter, 1), "Survey creation unsuccessful"
        session.close()

    def testNonExistent(self):
        counter = 0

        session = self.database.session()
        rowset = session.query(Survey).filter(Survey.title == "S_TITLE").all()
        for survey in rowset:
            counter = 1
        self.assertEqual(counter, 0), "Survey found despite non existing."
        session.close()

    def testSameCourse(self):
        counter = 0

        q_id = self.database.add_question("Q_TITLE" , 1, [123, "1"])
        self.database.add_course("TEST1001" , "1s1")
        self.database.add_survey("S1_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])
        self.database.add_survey("S2_TITLE" , "TEST1001 1s1" , [{"id" : q_id, "type" : "choice"}])

        session = self.database.session()
        rowset = session.query(Survey).filter(Survey.title == "S_TITLE").all()
        for survey in rowset:
            counter = 1
        self.assertEqual(counter, 0), "Survey created successfully despite a current survey already being affilited with the same course"


    def testNoQuestions(self):
        counter = 0

        self.database.add_course("TEST1001" , "1s1")
        self.database.add_survey("S1_TITLE" , "TEST1001 1s1" , [])

        session = self.database.session()
        rowset = session.query(Survey).filter(Survey.title == "S_TITLE").all()
        for survey in rowset:
            counter = 1
        self.assertEqual(counter, 0), "Survey created successfully despite having no questions."

if __name__ == '__main__':
    unittest.main()
