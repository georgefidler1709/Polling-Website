from scripts.base import *

ADMIN = 4
STAFF = 3
STUDENT = 2
GUEST = 1
UNREGISTERED = 0

# Generic class for a user login
class User(Base):
	__tablename__ = "users"
	username = Column(String(20), primary_key=True)
	password = Column(String(32), nullable=False)
	permissions = Column(Integer, nullable=False)
	courses = relationship("Enrolment", back_populates="student")
