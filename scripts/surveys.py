from scripts.base import *
from scripts.courses import *

CHOICE = 0
TEXT = 1

REVIEW = 0
OPEN = 1
CLOSED = 2

# Object that stores a singular question
class Question(Base):
	__tablename__ = "questions"
	id = Column(Integer, primary_key=True, default=newid)
	title = Column(String(), nullable=False)
	mandatory = Column(Boolean, nullable=False)
	available = Column(Boolean, nullable=False)
	surveys = relationship("SurveyQuestionLink", back_populates="question")
	options = relationship("Option", back_populates="question")

# Object that stores a survey which includes a link to all included questions
class Survey(Base):
	__tablename__ = "surveys"
	id = Column(Integer, primary_key=True, default=newid)
	course_id = Column(String(), nullable=False)
	course_semester = Column(String(), nullable=False)
	ForeignKeyConstraint([course_id, course_semester],
                         [Course.id, Course.semester])
	course = relationship(Course, foreign_keys = [course_id, course_semester])
	title = Column(String(), nullable=False)
	status = Column(Integer, nullable=False)
	questions = relationship("SurveyQuestionLink", back_populates="survey")
	completions = relationship("StudentCompletion", back_populates="survey")

class Option(Base):
	__tablename__ = "options"
	id = Column(Integer, primary_key=True, default=newid)
	question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
	question = relationship(Question, back_populates="options")
	title = Column(String(), nullable=False)
	UniqueConstraint(question_id, title)

class SurveyQuestionLink(Base):
	__tablename__ = "survey_question"
	id = Column(Integer, primary_key=True, default=newid)
	question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
	question = relationship("Question", back_populates="surveys")
	survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
	survey = relationship("Survey", back_populates="questions")
	number = Column(Integer, nullable=False)
	type = Column(Integer, nullable=False)
	#mandatory = Column(Boolean, nullable=False)
