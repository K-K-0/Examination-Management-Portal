from flask import Flask
from models import db, User, Booking, Course, Examination, ExaminationSlot, Rubric
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager , login_user, login_required, logout_user, current_user
from datetime import datetime

# app = Flask(__name__)
app = Flask(__name__, instance_relative_config=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Nothing"

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

auth = Blueprint('auth', __name__)

    
@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(email=email).first():
            flash('username already registered')
            return redirect(url_for('auth.register'))
        
        new_user = User(name=name,email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successfully. pls login')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html') 
    
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if not user:
            flash('Invalid credentials')
            return redirect(url_for("auth.login"))
        
        login_user(user)
        flash('logged in successfully')
    
        print("hello")
        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif user.role == "examiner":
            return redirect(url_for("examiner_dashboard"))
        
        return redirect(url_for("student_dashboard"))  
        
    return render_template("login.html")


@app.route("/admin/courses")
@login_required
def view_courses():
    if current_user.role != 'admin':
        return redirect(url_for("auth.login"))

    courses = Course.query.all()
    return render_template("admin/courses.html", courses=courses)

@app.route("/admin/courses/add", methods=["GET", "POST"])
@login_required

def add_courses():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    if request.method == "POST":
        course = Course(
            code=request.form["code"],
            name=request.form["name"],
            description=request.form["description"],
            status=request.form["status"]
        )

        db.session.add(course)
        db.session.commit()

        flash("course added successfully", "success")
        return redirect(url_for("view_courses"))

    return render_template("admin/add_courses.html")

@app.route("/admin/courses/edit/<int:id>", methods=["GET", "POST"])
@login_required

def edit_course(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    course = Course.query.get_or_404(id)
    
    if request.method == "POST":
        
        course.code=request.form["code"]
        course.name=request.form["name"]
        course.description=request.form["description"]
        course.status=request.form["status"]

        db.session.commit()

        flash("course updated successfully", "success")
        return redirect(url_for("view_courses"))

    return render_template("admin/edit_course.html", course=course)

@app.route("/admin/course/delete/<int:id>")
@login_required
def delete_course(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()

    flash("course deleted successfully", "success")
    return redirect(url_for("view_courses"))




@app.route("/admin/examination")
@login_required
def view_examinations():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    examinations = Examination.query.all()
    print(examinations)

    return render_template("admin/examinations.html", examinations=examinations)


@app.route("/admin/examination/add", methods=["GET", "POST"])
@login_required
def add_examinations():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    courses = Course.query.all()

    if request.method == "POST":

        exam = Examination(
            course_id=int(request.form["course_id"]),
            name=request.form["name"],
            exam_type=request.form["exam_type"],
            duration=int(request.form["duration"]),
            max_marks=int(request.form["max_marks"]),
            slot_creation_start=datetime.strptime(request.form["slot_start"], '%Y-%m-%d').date(),
            slot_creation_end=datetime.strptime(request.form["slot_end"], '%Y-%m-%d').date(),
            booking_start=datetime.strptime(request.form["booking_start"], '%Y-%m-%d').date(),
            booking_end=datetime.strptime(request.form["booking_end"], '%Y-%m-%d').date(),
            status=request.form["status"]
        )

        db.session.add(exam)
        db.session.commit()

        flash("exam created successfully", "success")

        return redirect(url_for("view_examinations"))

    return render_template("admin/add_examination.html", courses=courses)

@app.route("/admin/examination/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_examinations(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    exam = Examination.query.get_or_404(id)
    courses = Course.query.all()

    if request.method == "POST":

        
        exam.course_id=request.form["course_id"],
        exam.name=request.form("name"),
        exam.exam_type=request.form["exam_type"],
        exam.duration=request.form["duration"],
        exam.max_marks=request.form["max_marks"],
        exam.slot_creation_start=request.form["slot_start"],
        exam.slot_creation_end=request.form["slot_end"],
        exam.booking_start=request.form["booking_start"],
        exam.booking_end=request.form["booking_end"],
        exam.status=request.form["status"]

        
        db.session.commit()

        flash("exam updated successfully", "success")

        return redirect(url_for("view_examinations"))

    return render_template("admin/add_examination.html", courses=courses, exam=exam)


@app.route("/admin/examination/delete/<int:id>")
@login_required
def delete_examinations(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    exam = Examination.query.get_or_404(id)

    db.session.delete(exam)
    db.session.commit()

    flash("exam deleted successfully", "success")

    return redirect(url_for("view_examinations"))



@app.route("/admin/rubrics")
@login_required
def view_rubrics():
    if current_user.role != 'admin':
        return redirect(url_for("login"))
    rubrics = Rubric.query.all()

    return render_template("admin/rubrics.html", rubrics=rubrics)


@app.route("/admin/rubrics/add", methods=["GET", "POST"])
@login_required
def add_rubrics():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    exam = Examination.query.all()

    if request.method == "POST":

        rubric = Rubric(
            examination_id=request.form["exam"],
            criterion=request.form["criterion"],
            max_marks=request.form["max_marks"],
            weightage=request.form["weightage"],
            description=request.form["description"]
        )

        db.session.add(rubric)
        db.session.commit()

        flash("rubric created successfully")

        return redirect(url_for("view_rubrics"))

    return render_template("admin/add_rubrics.html", exam=exam)

@app.route("/admin/rubrics/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_rubrics(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    exam = Examination.query.all()
    rubric = Rubric.query.get_or_404(id)

    if request.method == "POST":

        
        rubric.examination_id=request.form["exam"],
        rubric.criterion=request.form["criterion"],
        rubric.max_marks=request.form["max_marks"],
        rubric.weightage=request.form["weightage"],
        rubric.description=request.form["description"]
        
        db.session.commit()

        flash("rubric updated successfully")

        return redirect(url_for("view_rubrics"))

    return render_template("admin/edit_rubric.html", exam=exam, rubric=rubric)


@app.route("/admin/rubrics/delete/<int:id>")
@login_required
def delete_rubrics(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))
    
    rubric = Rubric.query.get_or_404(id)
    db.session.delete(rubric)
    db.session.commit()

    flash("Rubric deleted successfully")

    return redirect(url_for("view_rubrics"))


@app.route("/admin/examiner")
@login_required
def view_examiners():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    examiners = User.query.filter_by(role="examiner").all()

    return render_template("admin/examiner.html", examiners=examiners)


@app.route("/admin/examiner/approve/<int:id>")
@login_required
def approve_examiner(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    examiner = User.query.get_or_404(id)

    examiner.is_examiner = True

    db.session.commit()

    flash("Examiner Approved successfelly")

    return redirect(url_for("view_examiners"))


@app.route("/admin/examiner/disapprove/<int:id>")
@login_required
def disapprove_examiner(id):
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    examiner = User.query.get_or_404(id)

    examiner.is_examiner = False

    db.session.commit()

    flash("Examiner Rejected")

    return redirect(url_for("view_examiners"))



@app.route("/examiner/dashboard")
@login_required
def examiner_dashboard():
    if current_user.role != 'examiner':
        return redirect(url_for("login"))

    examinations = Examination.query.filter_by(examiner_id=current_user.id).all()
    slots = ExaminationSlot.query.filter_by(examiner_id=current_user.id).all()

    return render_template("examiner/dashboard.html", examinations=examinations, slots=slots)


@app.route("/examiner/create-slot", methods=["GET", "POST"])
@login_required
def create_exam_slot():

    if current_user.role != "examiner":
        return redirect(url_for("login"))

    examinations = Examination.query.filter_by(
        examiner_id=current_user.id
    ).all()

    if request.method == "POST":

        exam_id = request.form.get("examination")

        if not exam_id:
            flash("Please select an examination.", "danger")
            return render_template(
                "examiner/add_slot.html",
                examinations=examinations
            )

        examination = Examination.query.get_or_404(int(exam_id))

        from datetime import datetime

        current_date = datetime.now().date()

        if current_date < examination.slot_creation_start:
            flash("Slot creation period has not started.", "danger")
            return redirect(url_for("create_exam_slot"))

        if current_date > examination.slot_creation_end:
            flash("Slot creation period has ended.", "danger")
            return redirect(url_for("create_exam_slot"))

        slot = ExaminationSlot(
            examination_id=examination.id,
            examiner_id=current_user.id,
            date=datetime.strptime(
                request.form["date"],
                "%Y-%m-%d"
            ).date(),
            start_time=datetime.strptime(
                request.form["start_time"],
                "%H:%M"
            ).time(),
            end_time=datetime.strptime(
                request.form["end_time"],
                "%H:%M"
            ).time(),
            capacity=int(request.form["capacity"]),
            available_seats=int(request.form["capacity"]),
            status="Open"
        )

        db.session.add(slot)
        db.session.commit()

        flash("Slot created successfully!", "success")

        return redirect(url_for("examiner_dashboard"))

    return render_template(
        "examiner/add_slot.html",
        examinations=examinations
    )


@app.route("/examiner/slot/edit/<int:id>", methods=["POST", "GET"])
@login_required
def edit_slot(id):
    if current_user.role != 'examiner':
        return redirect(url_for("login"))

    

    slot = ExaminationSlot.query.get_or_404(id)
    

    if request.method == "POST":

        examination = slot.examination

        if examination.examiner_id != current_user.id:
            flash("You are not assigned to this examination.", "danger")
            return redirect(url_for("examiner_dashboard"))

        from datetime import datetime

        current_date = datetime.now().date()

        if current_date < examination.slot_creation_start:
            flash("Slot creation period has not started.", "danger")
            return redirect(url_for("examiner_dashboard"))

        if current_date < examination.slot_creation_end:
            flash("Slot creation period has ended.", "danger")
            return redirect(url_for("examiner_dashboard"))

        slot_date = datetime.strptime(
            request.form["date"],
            "%Y-%m-%d"
        ).date()

        start_time = datetime.strptime(
            request.form["start_time"],
            "%H:%M"
        ).time()

        end_time = datetime.strptime(
            request.form["end_time"],
            "%H:%M"
        ).time()
        new_capacity = int(request.form["ccapacity"])
        booked_count = len(slot.bookings)

        if new_capacity < booked_count:
            flash(
                "Capacity cannot be less than already booked students.",
                "danger"
            )
            return redirect(url_for("edit_slot", id=id))
        
        slot.capacity = new_capacity
        slot.available_seats = new_capacity - booked_count

        db.sesion.commit()

        flash("Slot updated successfully", "success")
        return redirect(url_for("examiner_dashboard"))
    return render_template("examiner/add_slot.html", slot=slot)


@app.route("/examiner/slot/delete/<int:id>", methods=["POST", "GET"])
@login_required
def delete_slot(id):
    if current_user.role != 'examiner':
        return redirect(url_for("login"))

    slot = ExaminationSlot.query.get_or_404(id)
    

    if request.method == "POST":

        examination = slot.examination

        if examination.examiner_id != current_user.id:
            flash("You are not assigned to this examination.", "danger")
            return redirect(url_for("examiner_dashboard"))

        from datetime import datetime

        current_date = datetime.now().date()

        if current_date < examination.slot_creation_start:
            flash("Slot creation period has not started.", "danger")
            return redirect(url_for("examiner_dashboard"))

        if current_date < examination.slot_creation_end:
            flash("Slot creation period has ended.", "danger")
            return redirect(url_for("examiner_dashboard"))

        if len(slot.bookings) > 0:
            flash("Don't delete slot that has already booked")
            return redirect(url_for("examiner_dashboard"))

        db.session.delete(slot)
        db.session.commit()

        flash("slot deleted successfully")
        return redirect(url_for("examiner_dashboard"))

    
@app.route("/student/dashboard")
@login_required
def student_dashboard():

    if current_user.role != "student":
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "").strip()

    if search:
        examinations = Examination.query.join(Course).filter(
            Examination.status == "Active",
            (
                Examination.name.ilike(f"%{search}%") |
                Course.name.ilike(f"%{search}%") | 
                Course.code.ilike(f"%{search}%")
            )
        ).all()
    else:
        examinations = Examination.query.filter_by(
            status="Active"
        ).all()

    return render_template(
        "student/dashboard.html",
        examinations=examinations,
        search=search
    )

@app.route("/student/exam/<int:id>/slots")
@login_required
def view_exam_slot(id):
    if current_user.role != "student":
        return redirect(url_for("login"))

    exam = Examination.query.get_or_404(id)

    slot = Examination.query.filter_by(
        examination_id=exam.id,
        status="Open"
    ).all()

    return render_template("student/slots.html", exam=exam, slot=slot)

@app.route("/student/slot/book/<int:slot_id>", methods=["POST"])
@login_required
def book_slot(slot_id):

    if current_user.role != "student":
        return redirect(url_for("login"))

    slot = ExaminationSlot.query.get_or_404(slot_id)
    exam = slot.examination

    current_date = datetime.now().date()

    if current_date < exam.booking_start:
        flash("Booking period has not started.", "danger")
        return redirect(
            url_for("view_exam_slots", exam_id=exam.id)
        )

    if current_date > exam.booking_end:
        flash("Booking period has ended.", "danger")
        return redirect(
            url_for("view_exam_slots", exam_id=exam.id)
        )

    if slot.status != "Open":
        flash("This slot is not available.", "danger")
        return redirect(
            url_for("view_exam_slots", exam_id=exam.id)
        )

    if slot.available_seats <= 0:
        slot.status = "Closed"
        db.session.commit()

        flash("This slot is full.", "danger")

        return redirect(
            url_for("view_exam_slots", exam_id=exam.id)
        )

    existing_booking = Booking.query.join(
        ExaminationSlot
    ).filter(
        Booking.student_id == current_user.id,
        ExaminationSlot.examination_id == exam.id,
        Booking.status == "Booked"
    ).first()

    if existing_booking:
        flash(
            "You have already booked a slot for this examination.",
            "danger"
        )

        return redirect(
            url_for("view_exam_slots", exam_id=exam.id)
        )

    booking = Booking(
        student_id=current_user.id,
        slot_id=slot_id,
        booking_date=datetime.now(),
        status="Booked",
        marks=None,
        note=None
    )

    db.session.add(booking)

    slot.available_seats -= 1

    if slot.available_seats == 0:
        slot.status = "Closed"

    db.session.commit()

    flash("Slot Booked Successfully!", "success")

    return redirect(
        url_for("view_exam_slots", exam_id=exam.id)
    )

@app.route("/students/bookings")
@login_required
def student_bookings():
    if current_user.role != "student":
        return redirect(url_for("login"))

    bookings = Booking.query.filter_by(
        student_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template("student/bookings.html", bookings=bookings)

@app.route("/student/booking/cancel/<int:id>", methods=["POST"])
@login_required
def cancel_booking(id):

    if current_user != "student":
        return redirect(url_for("login"))

    booking = Booking.query.get_or_404(id)
    if booking.status == "Cancelled":
        flash("This booking is already cancelled")
        return redirect(url_for("students_bookings"))
    booking.status = "Cancelled"

    booking.slot.available_seats += 1

    if booking.slot.status == "Closed" and booking.slot.available_seats > 0:
        booking.slot.status = "Open"

    db.session.commit()

    flash("Booking Cancelled Successfully")

    return redirect(url_for("student_bookings"))


@app.route("/examiner/slots")
@login_required
def examiner_slots():
    if current_user.role != "examiner":
        return redirect(url_for("login"))

    slots = ExaminationSlot.query.filter_by(
        examiner_id=current_user.id
    ).all()

    return render_template("examiner/slots.html", slots=slots)


@app.route("/examiner/slots/<int:id>/student")
@login_required
def slot_student(id):
    if current_user.role != "examiner":
        return redirect(url_for("login"))

    slot = ExaminationSlot.query.get_or_404(id)
    booking = Booking.query.filter_by(slot_id=slot.id, status="Booked").all()

    return render_template("examiner/students.html", slot=slot, booking=booking)


@app.route("/examiner/evaluate/<int:id>", methods=["GET", "POST"])
@login_required
def evaluate_student(id):
    if current_user.role != "examiner":
        return redirect(url_for("login"))

    booking = Booking.query.get_or_404(id)

    if request.method == "POST":

        booking.marks = request.form["marks"]
        booking.note  = request.form["note"]

        booking.status = "Completed"

        db.session.commit()

        flash("Evaluation Successfull")

        return redirect(url_for("slot_students", slot_id=booking.slot_id))

    return render_template("examiner/evaluate.html", booking=booking)


@app.route("/student/result")
@login_required
def student_results():
    if current_user.role != "student":
        return redirect(url_for("login"))

    bookings = Booking.query.filter(
        Booking.student_id == current_user.id,
        Booking.status == "Completed"
    ).all()

    return render_template("student/result.html", bookings=bookings)


@app.route("/admin/examination/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_examiner(id):
    if current_user.role != "admin":
        return redirect(url_for("login"))

    exam = Examination.query.get_or_404(id)
    examiners = User.query.filter_by(
        role="examiner",
        is_examiner=True
    ).all()

    if request.method == "POST":

        exam.examiner_id = request.form["examiner"]

        db.session.commit()

        flash("examiners Assigned")
        return redirect(url_for("view_examinations"))
    return render_template("admin/assign_examiner.html", exam=exam, examiners=examiners)


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        return redirect(url_for("login"))

    data = {
        "students": User.query.filter_by(role="student").count(),
        "examiners": User.query.filter_by(role="examiner").count(),
        "courses": Course.query.count(),
        "examinations": Examination.query.count(),
        "slots": ExaminationSlot.query.count(),
        "bookings": Booking.query.count()
    }

    return render_template(
        "admin/dashboard.html",
        data=data
    )


@app.route("/admin/search")
@login_required
def admin_search():

    if current_user.role != "admin":
        return redirect(url_for("login"))

    q = request.args.get("q","")

    students = User.query.filter(
        User.role=="student",
        User.name.ilike(f"{q}")
    ).all()

    examiners = User.query.filter(
        User.role=="examiner",
        User.name.ilike(f"{q}")
    ).all()

    examinations = Examination.query.filter(
        Examination.name.ilike(f"{q}")
    ).all()

    return render_template("admin/search.html", students=students, examiners=examiners, examinations=examinations, q=q)


@app.route("/admin/bookings")
@login_required
def admin_bookings():

    if current_user.role != "admin":
        return redirect(url_for("login"))

    bookings = Booking.query.all()

    return render_template("admin/bookings.html", bookins=bookings)

@app.route("/admin/slots")
@login_required
def admin_slots():

    if current_user.role != "admin":
        return redirect(url_for("login"))

    slots = ExaminationSlot.query.all()

    return render_template("admin/slots.html", slots=slots)

app.register_blueprint(auth)
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        from werkzeug.security import generate_password_hash
        admin = User(name='admin', email='admin@gmail.com', password='admin', role='admin')
        db.session.add(admin)
        db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)
