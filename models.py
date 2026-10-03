from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    is_examiner = db.Column(db.Boolean, default=False)

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False) 
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="Active")

class Examination(db.Model):
    __tablename__ = "examinations"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(30))
    duration = db.Column(db.Integer)
    max_marks = db.Column(db.Integer)
    slot_creation_start = db.Column(db.Date)
    slot_creation_end = db.Column(db.Date)
    booking_start = db.Column(db.Date)
    booking_end = db.Column(db.Date)
    status = db.Column(db.String(30))
    examiner = db.relationship(
        "User",
        foreign_keys=[examiner_id],
        backref="assigned_examinations"
    )

class Rubric(db.Model):
    __tablename__ = "rubrics"

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey("examinations.id"), nullable=False)
    criterion = db.Column(db.String(80))
    max_marks = db.Column(db.Integer)
    weightage = db.Column(db.Integer)
    description = db.Column(db.Text)

class ExaminationSlot(db.Model):
    __tablename__ = "slots"

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey("examinations.id"), nullable=False)
    examiner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date)
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    capacity = db.Column(db.Integer)
    available_seats = db.Column(db.Integer)
    status = db.Column(db.String(30), default="Available")
    examination = db.relationship(
        "Examination",
        backref="slots"
    )

    examiner = db.relationship(
        "User",
        foreign_keys=[examiner_id],
        backref="examiner_slots"
    )

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey("slots.id"), nullable=False)
    booking_date = db.Column(db.Date)
    status = db.Column(db.String(30), default="Booked")
    marks = db.Column(db.Integer)
    note = db.Column(db.Text)