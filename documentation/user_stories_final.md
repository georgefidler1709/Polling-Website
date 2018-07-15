# User Stories
As a member of teaching staff I want to be able to create online surveys to get feedback from my students so I can better the course I teach.
As a student I want to be able to give my teachers feedback on the courses I take so it can be tailored to better meet my needs and those of future students.

### US1 - Admin Account Login
#### Description
As an administrator I should be able to login to a unique account so that only authorised admins can create surveys and so only I can see the results of surveys I created.
#### Acceptance Criteria
 - Once authorised, administrators should be issued a username or password.
 - When these credentials are entered into the ‘account login’ page the admin should be logged into the system as their unique account.
 - If credentials are entered incorrectly a message will prompt the user to try again.
 - After login the admin should have access to survey creation, question creation and the results of all current surveys.
##### Estimation: 6 Priority: 5
---
### US2A - Creating Surveys
#### Description
As an administrator I should be able to post surveys of questions on a course so I can get feedback from students.
#### Acceptance Criteria
 - Once logged in, an admin should be able to access the ‘Survey Creation’ page.
 - An admin should be able to select any of the provided courses (all courses that do not already have a current survey associated with them) to be associated with this survey.
 - An admin should be able to type in the desired title for the new survey.
 - The admin should be able to select any number of questions previously created for the new survey from the optional or mandatory question pools.
 - If a title and at least one question have been selected upon hitting the ‘submit’ button the admin will be notified that the survey submission was acceptable.
 - If the survey submission is acceptable staff for the course should be able to review the survey.
 - If no title has been entered the admin will instead be prompted to enter a title.
 - If no questions are selected the admin will instead be prompted to select some questions.
##### Estimation: 8 Priority: 8
---
### US2B - Closing Surveys
#### Description
As an administrator I should be able to close a survey when there are enough responses.
#### Acceptance Criteria
 - An admin should have the option to close any currently open surveys.
 - Once a survey is closed its results should be visible to all students and staff enrolled in the course affiliated with the survey from a link on their dashboard.
 - Students should no longer be able to submit a response to the survey once it is closed.
 - Students, staff and admins should now be able to view results after the survey is closed.
##### Estimation: 3 Priority: 3
---
### US3 - Question Creation
#### Description
As an administrator I should be able to create questions that can be used in future surveys so I can get specific feedback from my students.
#### Acceptance Criteria
 - Once logged in, an admin should be able to access the ‘Question Creation’ page.
 - An admin should be able to type in a question in a given field.
 - An admin should be able to create any number of options for the given question.
 - If an admin tries to create a question without any question text they should be prompted to edit the question title.
 - If an admin tries to create a question with fewer than two options they should be prompted to add more options for the question.
 - If an admin tries to create a question with multiple equal options they should be prompted to modify the available options.
 - Once the admin presses the ‘submit’ button, the question they have just created should be accessible from the “Survey Creation” page.
##### Estimation: 6 Priority: 7
---
### US4A - Student Login
#### Description
As a student I should be able to log in so that I can access parts of the site that are relevant to me.
#### Acceptance Criteria
 - On accessing the site a student will be prompted to enter their zID and zPass in appropriate fields.
 - Upon pressing 'submit' if a valid zID zPass combination were entered a student will be taken to their dashboard.
 - Upon pressing 'submit' if an invalid zID zPass combination were entered a student will be prompted to try again.
##### Estimation: 2 Priority: 5
---
### US4B - Survey Access
#### Description
As a student I should be able to access open surveys for courses that are relevant to me.
#### Acceptance Criteria
 - When a student opens their dashboard they will be able to see open surveys for all courses they are enrolled in.
 - A student must not be able to access a survey which they have already completed or which is linked with a course in which they are not enrolled.
 - If an admin or staff attempts to complete a survey, they will be redirected elsewhere.
##### Estimation 3 Priority: 8
---
### US4C - Students’ Completion of Survey
#### Description
As a student, I should be able to methodically fill in the survey questions, so that my response can be seen by other members of staff.
#### Acceptance Criteria
 - If a given question is multiple choice, students should be able to click on an answer to a question to select it.
 - Student’s selected answer should be highlighted in a manner to indicate their selection.
 - If a student tries to select a second answer to a single question, the first choice will be deselected and the new choice selected, indicating only the most recent choice is selected.
 - If a given question is written answer, a student should be able to type into a given field.
 - Student’s should be able to press a ‘submit’ button to finalise their responses.
 - If an answer has been given for every mandatory question once the ‘submit’ button is clicked, their response is submitted and the student is notified as such.
 - If any mandatory question has not been answered the response will not be accepted and the student will be prompted to answer all questions.
##### Estimation: 7 Priority: 7
---
### US5A - Viewing responses
#### Description
As a student, staff member or administrator I would like to be able to view the results of a survey so the feedback they supply can be used to better a course.
#### Acceptance Criteria
 - An admin should be able to select a survey from a list of all current surveys to access the collated results for.
 - Staff should be able to select a survey from a list of all closed surveys relevant to their enrolled courses.
 - Students should be able to select a survey from a list of all closed surveys relevant to their enrolled courses.
 - For multiple choice questions, the viewer should be able to determine how many times each answer was submitted in a clear format (ie. a table).
 - For written response questions, the viewer should be able to read all responses submitted.
 - No user that is not logged in should be able to access these responses.
 - No user should be able to see who submitted what responses.
##### Estimation: 5 Priority: 5
---
### US5B - Graphical Report generation
#### Description
As an administrator I should be able to view results of survey questions in a graphical format that is clearly understandable.
#### Acceptance Criteria
 - When viewing responses to a survey the user should be able to click a “view charts” link.
 - Results to multiple choice questions should be displayed in a graphical format (pie chart) that is representative of the proportions of users which selected each response.
 - Results for text responses questions should be displayed in a list.
##### Estimation: 6 Priority: 2
---
### US6A - Staff Login
#### Description
As a staff member, I should be able to access surveys relevant to the courses I teach so the questions and results can be reviewed.
#### Acceptance Criteria
 - On accessing the site a staff member will be prompted to enter their staff-ID and password in appropriate fields.
 - Upon pressing 'submit' if a valid staff-Id and password combination were entered a staff member should be taken to their dashboard.
 - Upon pressing 'submit' if an invalid staff-Id and password combination were entered a staff member will be prompted to try again.
 - Once successfully logged in staff should be able to access a dashboard which shows links to results for closed surveys for their courses and links to review/edit unreviewed surveys for their courses.
##### Estimation: 5 Priority: 6
---
### US6B - Staff Survey Review
#### Description
As a staff member in charge of a given course, I should be able to modify and approve a survey before it is open for students for my courses.
#### Acceptance Criteria
 - Once created by an admin, links to surveys should appear on the dashboard of the staff members in charge of the appropriate course (chosen during survey creation).
 - Upon clicking these links staff should be able to see these surveys in their entirety.
 - Staff should be able to remove optional questions during the review process.
 - Staff should be able to add optional questions as either multiple choice or text response questions during the review process.
 - Staff should not be able to add or remove mandatory questions during the review process.
 - Staff should be able to approve the survey so that it is sent out to students of the given course.
##### Estimation: 4 Priority: 5
