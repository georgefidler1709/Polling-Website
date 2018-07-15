from scripts.base import *
from scripts.surveys import *
from scripts.users import *

# Object that holds a single users response to a survey
class Response(Base):
	__tablename__ = "responses"
	id = Column(Integer, primary_key=True, default=newid)
	survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
	survey = relationship(Survey)
	answers = relationship("Answer", back_populates="response")

class Answer(Base):
	__tablename__ = "answers"
	id = Column(Integer, primary_key=True, default=newid)
	response_id = Column(Integer, ForeignKey("responses.id"), nullable=True)
	response = relationship(Response)
	question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
	question = relationship(Question)
	link_id = Column(Integer, ForeignKey("survey_question.id"), nullable=False)
	link = relationship(SurveyQuestionLink)
	type = Column(String())

	__mapper_args__ = {
    	'polymorphic_identity':'none',
    	'polymorphic_on':type
    }

class AnswerChoice(Answer):
	__tablename__ = "answers_choice"
	id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
	option_id = Column(Integer, ForeignKey("options.id"), nullable=True)
	option = relationship(Option)

	__mapper_args__ = {
    	'polymorphic_identity':'choice',
    }

class AnswerText(Answer):
	__tablename__ = "answers_text"
	id = Column(Integer, ForeignKey('answers.id'), primary_key=True)
	text = Column(String(), nullable=False)

	__mapper_args__ = {
    	'polymorphic_identity':'text',
    }

class StudentCompletion(Base):
	__tablename__ = "student_survey"
	survey_id = Column(Integer, ForeignKey("surveys.id"), primary_key=True)
	survey = relationship(Survey)
	username = Column(String(), ForeignKey("users.username"), primary_key=True)
	student = relationship(User)
