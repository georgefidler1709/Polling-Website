from scripts.base import *

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(8), primary_key=True)
    semester = Column(String(4), primary_key=True)
    students = relationship("Enrolment", back_populates="course")
    survey = relationship("Survey", back_populates="course")

class Enrolment(Base):
    __tablename__ = "enrolments"
    username = Column(String(), ForeignKey("users.username"), primary_key=True)
    course_id = Column(String(), primary_key=True)
    course_semester = Column(String(), primary_key=True)
    ForeignKeyConstraint([course_id, course_semester],
                         [Course.id, Course.semester])
    course = relationship("Course", foreign_keys = [course_id, course_semester])
    student = relationship("User", back_populates="courses")
