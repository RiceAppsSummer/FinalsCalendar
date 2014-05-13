from app import db
from app.models import Course, Exam
import datetime

def setup_all():
    setup_db()
    setup_fake()

def setup_db():
    db.drop_all()
    db.create_all()

def setup_fake():
    fake_course1 = Course(department_name = "COMP", number = "182")
    fake_course2 = Course(department_name = "ECON", number = "201")

    fake_exam1 = Exam(start_time = datetime.datetime.today(), end_time = datetime.datetime.today(), course = fake_course1, section = "001", teacher = "Luay Nakleh", location = "KCK 100")
    fake_exam2 = Exam(start_time = datetime.datetime.today(), end_time = datetime.datetime.today(), course = fake_course2, section = "003", teacher = "John Diamond", location = "HRZ AMP")
    db.session.add_all([fake_course1,fake_course2,fake_exam1,fake_exam2])
    db.session.commit()

if __name__ == "__main__":
    setup_all()

