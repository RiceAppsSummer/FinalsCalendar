from flask import render_template,jsonify
from app import app,db
import datetime
import json
import download
from app.models import Course,Exam
from collections import defaultdict

@app.route('/')
def test():
    return render_template("layout.html")

@app.route("/courses")
def courses():
	def create_inner_default_dict():
		return defaultdict(dict)

	mapping = defaultdict(create_inner_default_dict)
	courses_exams = db.session.query(Course,Exam).join(Course.exams)

	for course_exam in courses_exams:
		course_name = str(course_exam[0])
		teacher = course_exam[1].teacher
		section = course_exam[1].section
		s_time = course_exam[1].start_time.isoformat()
		e_time = course_exam[1].end_time.isoformat()
		mapping[course_name][teacher][section] = {"start_time":s_time,"end_time":e_time}

	return jsonify(**mapping)

	



