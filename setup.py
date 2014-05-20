from app import db
from app.models import Course, Exam
import datetime
import download

def setup_all():
    setup_db()
    setup_schedule()

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


def setup_schedule():
    unaltered_sched = download.strip_schedule()
    for item in unaltered_sched:
        course_array = item["course"].split(" ")
        course = db.session.query(Course).filter_by(department_name = course_array[0], number = course_array[1]).first()
        if course is None:
            course = Course(department_name = course_array[0], number = course_array[1])
            db.session.add(course)


        def double_split():
            for once in item["date"].split(','):
                for twice in once.split():
                    if twice != '':
                        yield twice

        def process_time(time_string):
            if time_string == "Noon":
                return "12:00pm"
            parts = time_string.split(":")
            if len(parts[0])<2:
                time_string="0"+time_string
            return time_string

        date_array = list(double_split())
        date_array.pop(0)
        if len(date_array[1])<2:
            date_array[1]="0"+date_array[1]
        time_array = map(process_time,item["time"].split(" - "))
        start_time,end_time = time_array
        



        ex_start = datetime.datetime.strptime(" ".join(date_array)+" "+start_time, "%b %d %Y %I:%M%p")
        ex_end = datetime.datetime.strptime(" ".join(date_array)+" "+end_time, "%b %d %Y %I:%M%p")
        exam = Exam(start_time = ex_start, end_time = ex_end, course = course, section = course_array[2], teacher = item["instructor"], location = item["room"])

        db.session.add(exam)
        db.session.commit()


if __name__ == "__main__":
    setup_all()

