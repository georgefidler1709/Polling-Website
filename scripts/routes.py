from flask import Flask, session, redirect, render_template, request, url_for, flash
from scripts.database import *
import scripts.authentication as authentication

# Index page with link to logon
@app.route("/")
def route_index():
    if "username" in session:
        return redirect(url_for("route_dashboard"))
    return redirect(url_for("route_login"))

# Login page
@app.route("/login/", methods = ["GET", "POST"])
def route_login():
    if request.method == "POST":
        json_data = request.get_json()
        user = authentication.login(request.form["username"], request.form["password"])
        if user:
            session["username"] = user.username
            session["permissions"] = user.permissions
            return redirect(url_for("route_dashboard"))
        else:
            flash("Incorrect Login Info")

    return render_template("login.html")

@app.route("/register_guest/", methods = ["GET", "POST"])
def route_register_guest():
    if request.method == "POST":
        status = database.add_user(request.form["username"], request.form["password"], UNREGISTERED)
        if status:
            course_id, course_semester = request.form["offering"].split(" ")
            database.add_enrolment(request.form["username"], course_id, course_semester)
            flash("Registration request successfully sent")
        else:
            flash("Username already exists")
    return render_template("register_guest.html", offerings = database.get_courses())

@app.route("/approve/<username>")
@authentication.require_permissions(ADMIN)
def route_approve_registration(username):
    database.promote(username, GUEST)
    return redirect(url_for("route_dashboard"))


# Admin dashboard with links to create surveys and questions
@app.route("/dashboard/")
@authentication.require_permissions(ADMIN, STAFF, STUDENT, GUEST, UNREGISTERED)
def route_dashboard():
    if session["permissions"] == ADMIN:
        surveys = database.get_surveys()
        return render_template("dashboard_admin.html", surveys=surveys, requests=database.get_registration_requests())
    if session["permissions"] == STAFF:
        review = database.get_viewable(session["username"], REVIEW)
        view = database.get_viewable(session["username"], CLOSED)
        return render_template("dashboard_staff.html", view=view, review=review)
    if session["permissions"] == STUDENT or session["permissions"] == GUEST:
        complete = database.get_completeable(session["username"])
        view = database.get_viewable(session["username"], CLOSED)
        return render_template("dashboard_student.html", complete=complete, view=view)
    return render_template("dashboard_unapproved.html")

@app.route("/logout/")
def route_logout():
    if "permissions" in session: del session["permissions"]
    if "username" in session: del session["username"]
    return redirect(url_for("route_login"))

# Page to create surveys
@app.route("/create_survey/", methods = ["GET", "POST"])
@authentication.require_permissions(ADMIN)
def route_create_survey():
    if request.method == "POST":
        json_data = request.get_json()
        obj_id = database.add_survey(**json_data)
    return render_template("create_survey.html", questions = database.get_questions(), offerings = database.get_courses(no_survey=True))

@app.route("/create_survey/done/")
@authentication.require_permissions(ADMIN)
def route_create_survey_done():
    return render_template("create_survey_done.html")

@app.route("/edit_survey/<survey_id>/", methods = ["GET", "POST"])
@authentication.require_permissions(STAFF)
def route_edit_survey(survey_id):
    survey = database.get_surveys(int(survey_id))
    survey_questions = database.get_questions(survey=survey)
    questions = database.get_questions()
    if request.method == "POST":
        json_data = request.get_json()
        add = json_data["toAdd"]
        remove = json_data["toDelete"]
        database.edit_survey(survey, remove, add)
        database.change_survey_status(survey, OPEN)
        return redirect(url_for("route_survey_approved"))
    return render_template("edit_survey.html", questions=questions, survey_questions=survey_questions, survey=survey)

@app.route("/survey_approved/")
@authentication.require_permissions(STAFF)
def route_survey_approved():
    return render_template("survey_approved.html")

# Page to create questions
@app.route("/create_question/", methods = ["GET", "POST"])
@authentication.require_permissions(ADMIN)
def route_create_question():
    if request.method == "POST":
        title = request.form["title"]
        mandatory = "mandatory" in request.form
        options = []
        for i, option in sorted(request.form.items(), key = lambda x: x[0]):
            if i not in ["mandatory", "title"] and option != "":
                options.append(option)
        obj_id = database.add_question(title, mandatory, options)
        return redirect(url_for("route_create_question_success", question_id=obj_id))
    return render_template("create_question.html")

@app.route("/create_question/<question_id>/success/")
@authentication.require_permissions(ADMIN)
def route_create_question_success(question_id):
    return render_template("create_question_success.html", question=database.get_questions(int(question_id)))

# Page to view a list of surveys to get their shareable links and results (now just redirects to dashboard)
@app.route("/survey_list/")
def route_survey_list():
    return redirect(url_for("route_dashboard"))

@app.route("/question_list/", methods = ["GET", "POST"])
@authentication.require_permissions(ADMIN)
def route_question_list():
    questions = database.get_questions()
    if request.method == "POST":
        database.remove_questions(request.form.keys())
        return redirect(url_for("route_dashboard"))
    return render_template("view_questions.html", questions=questions)

# Page to respond to a survey
@app.route("/survey/<survey_id>/", methods = ["GET", "POST"])
@authentication.require_permissions(STUDENT, GUEST)
def route_response(survey_id):
    survey = database.get_surveys(int(survey_id))
    questions = database.get_questions(survey=survey)
    completeable = [x.id for x in database.get_completeable(session["username"])]
    if survey.id not in completeable:
        return redirect(url_for("route_dashboard"))
    question_ids = [l.number for q,l in questions]
    #mandatory_ids = [l.number for q,l in questions if l.mandatory]
    if request.method == "POST":
        # print("Got here")
        survey_successful = True
        answers = []
        for q, l in questions:
            if str(l.number) in request.form:
                if l.type == "choice":
                    answers.append((q,l, int(request.form[str(l.number)])))
                else:
                    answers.append((q,l, request.form[str(l.number)]))
            # elif l.mandatory: # Mandatory question unanswered
            #     survey_successful = False
            #     flash("All mandatory questions must be completed")
            #     break
        if survey_successful:
            database.add_response(session["username"], survey, answers)
            return redirect(url_for("route_response_success", survey_id = survey_id))
    return render_template("response.html", question_ids = question_ids, survey = survey, questions = questions, mandatory=[l.number for q, l in questions if q.mandatory])

# Page to show that a response has been successful
@app.route("/survey/<survey_id>/success/")
def route_response_success(survey_id):
    return render_template("survey_accepted.html", title = database.get_surveys(int(survey_id)).title)

# Page to view collated results from a survey
@app.route("/view_results/<survey_id>/", methods = ["GET", "POST"])
@authentication.require_permissions(ADMIN, STUDENT, STAFF, GUEST)
def route_view_results(survey_id):
    survey = database.get_surveys(int(survey_id))
    if survey.status != CLOSED and session["permissions"] != ADMIN:
        return redirect(url_for("route_dashboard"))

    if request.method == "POST":
        database.change_survey_status(survey, CLOSED)
        return render_template("survey_closed.html")

    data = database.get_survey_responses(survey)
    return render_template("view_results.html", survey=survey, data=data, perms=session["permissions"], admin=session["permissions"] == ADMIN, CLOSED=CLOSED)

@app.route("/view_charts/<survey_id>/", methods = ["GET", "POST"])
@authentication.require_permissions(ADMIN, STUDENT, STAFF, GUEST)
def route_view_charts(survey_id):
    survey = database.get_surveys(int(survey_id))
    if survey.status != CLOSED and session["permissions"] != ADMIN:
        return redirect(url_for("route_dashboard"))

    data = database.get_survey_responses(survey)
    return render_template("view_charts.html", survey=survey, data=data, perms=session["permissions"], admin=session["permissions"] == ADMIN, CLOSED=CLOSED)
