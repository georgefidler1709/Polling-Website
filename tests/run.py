import os
from scripts.routes import app, database

if not os.path.exists("data"):
	os.makedirs("data")
database.open('sqlite:///data/survey_database.db')

print("ADDING ADMIN")
database.add_user("admin", "password", 4)

print("ADDING STAFF")
database.mass_add_users("data/passwords.csv")

print("ADDING COURSES")
database.mass_add_courses("data/courses.csv")

print("ENROLLING USERS")
database.mass_enrol("data/enrolments.csv")


print("STARTING...")
app.config["SECRET_KEY"] = "f09a-jerome"
app.run(debug=True)
