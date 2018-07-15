from scripts.base import *
from flask import Flask

from scripts.users import *
from scripts.courses import *
from scripts.surveys import *
from scripts.responses import *

# Class to maintain links to all other objects and read data from files
class Database:
	def open(self, path):
		self.engine = create_engine(path)
		Base.metadata.create_all(self.engine)
		Base.metadata.bind = self.engine
		self.session = sessionmaker(bind=self.engine)

	def add_row(self, session, row):
		session.add(row)
		session.commit()
		session.close()

	def add_user(self, username, password, permissions):
		session = self.session()
		user = session.query(User.username).filter(User.username == username)
		if not session.query(user.exists()).scalar():
			user = User(username=username, password=password, permissions=permissions)
			username = user.username
			self.add_row(session, user)
			return username
		else:
			return False

	def add_course(self, course_id, semester):
		session = self.session()
		course = Course(id=course_id, semester=semester)
		self.add_row(session, course)

	def add_enrolment(self, username, course_id, course_semester):
		session = self.session()
		enrolment = Enrolment(username=username, course_id=course_id, course_semester=course_semester)
		self.add_row(session, enrolment)

	def add_question(self, title, mandatory, options = []):
		session = self.session()
		question = Question(title=title, mandatory=mandatory, available=True)
		session.add(question)
		session.commit()
		question_id = question.id
		for o in options:
			option = Option(question_id=question_id, title=o)
			session.add(option)
		session.commit()
		session.close()
		return question_id

	def remove_questions(self, ids):
		session = self.session()
		questions = self.get_questions(question_id=ids)
		for q in questions:
			q.available = False
			session.add(q)
		session.commit()
		session.close()

	def add_survey(self, title, course, questions):
		if len(questions) < 1:
			return False
		session = self.session()
		course_id, course_semester = course.split()
		already = session.query(Survey).filter(Survey.course_id == course_id, Survey.course_semester == course_semester).all()
		if len(already) > 0: return False
		survey = Survey(title=title, course_id=course_id, course_semester=course_semester, status=REVIEW)
		session.add(survey)
		session.commit()
		survey_id = survey.id
		print(questions)
		for i, q in enumerate(questions):
			link = SurveyQuestionLink(question_id=q["id"], survey_id=survey_id, number=i, type=q["type"])
			session.add(link)
		session.commit()
		session.close()
		return survey_id

	def edit_survey(self, survey, delete, add):
		session = self.session()
		deleted = session.query(SurveyQuestionLink).filter(SurveyQuestionLink.id.in_(delete)).all()
		for d in deleted:
			session.delete(d)
		current = database.get_questions(survey=survey)
		end = max(current, key=lambda x: x[1].number)
		for i, q in enumerate(add):
			link = SurveyQuestionLink(question_id=q["id"], survey_id=survey.id, number=end[1].number+i, type=q["type"])
			session.add(link)
		session.commit()
		session.close()

	def add_response(self, username, survey, answers):
		session = self.session()
		completion = StudentCompletion(username=username, survey_id=survey.id)
		session.add(completion)
		response = Response(survey_id=survey.id)
		session.add(response)
		for q, l, a in answers:
			if l.type == "choice":
				response.answers.append(AnswerChoice(question_id=q.id, link_id=l.id, option_id=a))
			else:
				response.answers.append(AnswerText(question_id=q.id, link_id=l.id, text=a))
		session.commit()
		session.close()

	def change_survey_status(self, survey, status):
		session = self.session()
		survey = session.query(Survey).filter(Survey.id == survey.id).one()
		survey.status = status
		session.commit()
		session.close()

	def get_questions(self, question_id = None, survey = None):
		session = self.session()
		if survey:
			link_ids = [link.question_id for link in session.query(SurveyQuestionLink).filter(SurveyQuestionLink.survey == survey).all()]
			questions = session.query(Question, SurveyQuestionLink).filter(Question.id.in_(link_ids), SurveyQuestionLink.survey_id == survey.id).join(SurveyQuestionLink).options(joinedload(Question.options)).all()
			questions.sort(key=lambda x: x[1].number)
		elif question_id != None :
			if isinstance(question_id, int):
				questions = session.query(Question).filter(Question.id == question_id).options(joinedload(Question.options)).all()
			else:
				questions = session.query(Question).filter(Question.id.in_(question_id)).options(joinedload(Question.options)).all()
		else:
			questions = session.query(Question).filter(Question.available == True).options(joinedload(Question.options)).all()
		session.close()
		return questions

	def get_completeable(self, user_id):
		session = self.session()
		surveys = session.query(Survey).filter(~Survey.completions.any(StudentCompletion.username == user_id),
		 										Survey.course.has(Course.students.any(Enrolment.username == user_id)),
												Survey.status == OPEN).all()
		session.close()
		return surveys

	def get_viewable(self, user_id, status):
		session = self.session()
		surveys = session.query(Survey).filter(	Survey.course.has(Course.students.any(Enrolment.username == user_id)),
												Survey.status == status).all()
		session.close()
		return surveys

	def get_courses(self, no_survey=False):
		session = self.session()
		if no_survey:
			courses = session.query(Course).filter(Course.survey == None).all()
		else:
			courses = session.query(Course).all()
		session.close()
		return courses

	def get_surveys(self, obj_id = None):
		session = self.session()
		if obj_id:
			surveys = session.query(Survey).filter(Survey.id == obj_id).one()
		else:
			surveys = session.query(Survey).all()
		session.close()
		return surveys

	def get_survey_responses(self, survey):
		session = self.session()
		responses = session.query(Response).filter(Response.survey_id == survey.id).all()
		questions = database.get_questions(survey=survey)
		results = {l.id : {option.id : 0 for option in q.options} if l.type == "choice" else [] for q, l in questions}
		for r in responses:
			for answer in r.answers:
				if answer.type == "choice":
					results[answer.link_id][answer.option_id] += 1
				else:
					results[answer.link_id].append(answer.text)
		session.close()
		return {"results": results, "questions": questions}

	def get_registration_requests(self):
		session = self.session()
		guests = session.query(User).filter(User.permissions == UNREGISTERED).options(joinedload(User.courses)).all()
		session.close()
		return guests

	def promote(self, username, permissions):
		session = self.session()
		user = session.query(User).filter(User.username == username).one()
		user.permissions = permissions
		session.add(user)
		session.commit()
		session.close()

	def mass_add_users(self, filename):
		session = self.session()
		f = open(filename)
		users = []
		roles = {"student": STUDENT, "staff": STAFF}
		current = session.query(User.username).all()
		for user in f.readlines():
			username, password, role = user.strip().split(",")
			if not (username,) in current:
				users.append(User(username=username, password=password, permissions=roles[role]))
				current.append((username,))
		session.bulk_save_objects(users)
		session.commit()
		session.close()

	def mass_add_courses(self, filename):
		session = self.session()
		f = open(filename)
		courses = []
		current = session.query(Course.id, Course.semester).all()
		for course in f.readlines():
			id, semester = course.strip().split(",")
			if not (id, semester) in current:
				courses.append(Course(id=id, semester=semester))
				current.append((id, semester))
		session.bulk_save_objects(courses)
		session.commit()
		session.close()

	def mass_enrol(self, filename):
		session = self.session()
		f = open(filename)
		enrolments = []
		current = session.query(Enrolment.username, Enrolment.course_id, Enrolment.course_semester).all()
		for enrolment in f.readlines():
			username, course_id, semester = enrolment.strip().split(",")
			if not (username, course_id, semester) in current:
				enrolments.append(Enrolment(username=username, course_id=course_id, course_semester=semester))
				current.append((username, course_id, semester))
		session.bulk_save_objects(enrolments)
		session.commit()
		session.close()


app = Flask(__name__, static_folder='../static', template_folder='../templates')
database = Database()
