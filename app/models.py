from app import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer,primary_key=True)
    department_name = db.Column(db.String,nullable=False)
    number = db.Column(db.String,nullable=False)

    def __str__(self):
        return self.department_name+" "+self.number

    def __repr__(self):
        return str(self)    

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer,primary_key=True)
    start_time = db.Column(db.DateTime(timezone=False),nullable=False)
    end_time = db.Column(db.DateTime(timezone=False),nullable=False)
    
    course_id = db.Column(db.ForeignKey("courses.id"),nullable=False)
    course = db.relationship("Course",backref="exams")

    section = db.Column(db.String,nullable=False)
    teacher = db.Column(db.String,nullable=False)

    location = db.Column(db.String,nullable = False)

