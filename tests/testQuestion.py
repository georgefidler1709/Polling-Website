import unittest
from scripts.base import *
from flask import Flask
from scripts.database import *
from scripts.users import *
from scripts.courses import *
from scripts.surveys import *
from scripts.responses import *

OPTIONAL = 0
MANDATORY = 1

class testQuestion(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        self.database.open('sqlite:///data/UnitTest.db')

    def tearDown(self):
        Base.metadata.drop_all()

    def testMandatory(self):
        counter = 0

        self.database.add_question("TITLE" , MANDATORY, [123, "1"])

        session = self.database.session()
        rowset = session.query(Question).filter(Question.title == "TITLE").all()
        for question in rowset:
            self.assertEqual(question.mandatory, MANDATORY), "Question set to mandatory upon creation was not tagged mandatory for later i.e. will be treated as optional"
            counter = 1
        self.assertEqual(counter, 1), "Question not created at all"
        session.close()

    def testOptional(self):
        counter = 0

        self.database.add_question("TITLE" , OPTIONAL, [123, "1"])

        session = self.database.session()
        rowset = session.query(Question).filter(Question.title == "TITLE").all()
        for question in rowset:
            self.assertEqual(question.mandatory, MANDATORY), "Question set to mandatory upon creation was not tagged optional for later i.e. will be treated as mandatory"
            counter = 1
        self.assertEqual(counter, 1), "Question not created at all"
        session.close()

if __name__ == '__main__':
    unittest.main()
