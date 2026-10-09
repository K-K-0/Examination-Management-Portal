
from datetime import date, time, timedelta

from app import app
from models import (
    db,
    User,
    Course,
    Examination,
    Rubric,
    ExaminationSlot,
    Booking
)


with app.app_context():

    # Create tables if they do not exist
    db.create_all()

    # -------------------------
    # 1. USERS
    # -------------------------
    # Do not create an admin; your admin already exists.

    examiner = User.query.filter_by(
        email="examiner@example.com"
    ).first()

    if not examiner:
        examiner = User(
            name="Demo Examiner",
            email="examiner@example.com",
            password="Examiner@123",
            role="examiner",
            is_examiner=True
        )
        db.session.add(examiner)

    student = User.query.filter_by(
        email="student@example.com"
    ).first()

    if not student:
        student = User(
            name="Demo Student",
            email="student@example.com",
            password="Student@123",
            role="student",
            is_examiner=False
        )
        db.session.add(student)

    db.session.commit()

    # -------------------------
    # 2. COURSES
    # -------------------------

    course_data = [
        {
            "code": "CS101",
            "name": "Introduction to Programming",
            "description": "Programming fundamentals and problem solving.",
            "status": "Active"
        },
        {
            "code": "CS201",
            "name": "Data Structures and Algorithms",
            "description": "Core data structures and algorithms.",
            "status": "Active"
        },
        {
            "code": "AI301",
            "name": "Machine Learning",
            "description": "Introduction to machine learning concepts.",
            "status": "Active"
        }
    ]

    for data in course_data:
        if not Course.query.filter_by(code=data["code"]).first():
            db.session.add(Course(**data))

    db.session.commit()

    # -------------------------
    # 3. EXAMINATIONS
    # -------------------------

    today = date.today()

    slot_start = today - timedelta(days=1)
    slot_end = today + timedelta(days=10)
    booking_start = today - timedelta(days=1)
    booking_end = today + timedelta(days=15)

    courses = {
        course.code: course
        for course in Course.query.all()
    }

    exam_data = [
        {
            "course_code": "CS101",
            "name": "Programming Viva",
            "exam_type": "Viva",
            "duration": 20,
            "max_marks": 100
        },
        {
            "course_code": "CS201",
            "name": "Data Structures Practical",
            "exam_type": "Practical",
            "duration": 30,
            "max_marks": 100
        },
        {
            "course_code": "AI301",
            "name": "Machine Learning Project Demo",
            "exam_type": "Project Demo",
            "duration": 30,
            "max_marks": 100
        }
    ]

    for data in exam_data:
        if not Examination.query.filter_by(
            name=data["name"],
            course_id=courses[data["course_code"]].id
        ).first():
            exam = Examination(
                course_id=courses[data["course_code"]].id,
                examiner_id=examiner.id,
                name=data["name"],
                exam_type=data["exam_type"],
                duration=data["duration"],
                max_marks=data["max_marks"],
                slot_creation_start=slot_start,
                slot_creation_end=slot_end,
                booking_start=booking_start,
                booking_end=booking_end,
                status="Active"
            )
            db.session.add(exam)

    db.session.commit()

    # -------------------------
    # 4. RUBRICS
    # -------------------------

    for exam in Examination.query.all():
        if not Rubric.query.filter_by(
            examination_id=exam.id
        ).first():

            if exam.exam_type == "Viva":
                criteria = [
                    ("Conceptual Understanding", 40, 40),
                    ("Communication", 30, 30),
                    ("Problem Solving", 30, 30)
                ]
            elif exam.exam_type == "Practical":
                criteria = [
                    ("Implementation", 40, 40),
                    ("Correctness", 40, 40),
                    ("Explanation", 20, 20)
                ]
            else:
                criteria = [
                    ("Project Design", 30, 30),
                    ("Technical Implementation", 40, 40),
                    ("Presentation", 30, 30)
                ]

            for criterion, marks, weightage in criteria:
                db.session.add(
                    Rubric(
                        examination_id=exam.id,
                        criterion=criterion,
                        max_marks=marks,
                        weightage=weightage,
                        description=f"Evaluate {criterion.lower()}."
                    )
                )

    db.session.commit()

    # -------------------------
    # 5. EXAMINATION SLOTS
    # -------------------------

    for exam in Examination.query.all():
        existing_slot = ExaminationSlot.query.filter_by(
            examination_id=exam.id,
            examiner_id=examiner.id
        ).first()

        if not existing_slot:
            db.session.add(
                ExaminationSlot(
                    examination_id=exam.id,
                    examiner_id=examiner.id,
                    date=today + timedelta(days=2),
                    start_time=time(10, 0),
                    end_time=time(10, 30),
                    capacity=5,
                    available_seats=5,
                    status="Open"
                )
            )

    db.session.commit()

    # -------------------------
    # 6. SAMPLE BOOKING
    # -------------------------

    slot = ExaminationSlot.query.first()

    if slot:
        existing_booking = Booking.query.filter_by(
            student_id=student.id,
            slot_id=slot.id
        ).first()

        if not existing_booking:
            db.session.add(
                Booking(
                    student_id=student.id,
                    slot_id=slot.id,
                    booking_date=today,
                    status="Booked",
                    marks=None,
                    note=None
                )
            )

            slot.available_seats = max(
                0, slot.available_seats - 1
            )

            if slot.available_seats == 0:
                slot.status = "Closed"

            db.session.commit()

    print("Seed data inserted successfully.")
    print("Existing admin account was not changed.")