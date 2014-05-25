from flask import render_template
from app import app,db
import datetime
import download
from app.models import Course,Exam


@app.route('/')
def test():
    return render_template("layout.html")

@app.route("/courses")
def courses():
	mapping = {"courseName":{"teacherName":{"section":[datetime.datetime.today()]}}}
	courses = db.session.query(Course,Exam.teacher).join(Course.exams).group_by(Exam.teacher)
	print list(courses)
	for course in courses:
		course_name = str(course[0])
		mapping[course_name] = {str(course[1])}

		# print course.exams.group_by(Exam.teacher)
		
	



