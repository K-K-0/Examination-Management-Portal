from flask import Flask
from models import db, User, Booking, Course, Examination, ExaminationSlot, Rubric
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import LoginManager , login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Nothing"

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


auth = Blueprint('auth', __name__)
    
@auth.route('/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(email=email).first():
            flash('username already registered')
            return redirect(url_for('register'))
        
        new_user = User(name=name,email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successfully. pls login')
        return redirect(url_for('login'))
    
    return render_template('register.html') 
    
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if not user:
            flash('Invalid credentials')
            return redirect(url_for('login'))
        
        login_user(user)
        flash('logged in successfully')
    
    
        if user.is_admin:
            return redirect(url_for('auth.admin_dashboard'))
        else:
            return redirect(url_for('auth.user_dashboard'))  
        
    return render_template('login.html')


@app.route("/admin/courses")
@login_required
def view_courses():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

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

    return render_template("admin/add_course.html")

@app.route("/admin/courses/edit/<int:id>", methods=["GET", "POST"])
@login_required

def edit_courses(id):
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

    return render_template("admin/examination.html", examinations=examinations)


@app.route("/admin/examination/add", methods=["GET", "POST"])
@login_required
def add_examinations():
    if current_user.role != 'admin':
        return redirect(url_for("login"))

    courses = Course.query.all()

    if request.method == "POST":

        exam = Examination(
            course_id=request.form["course_id"],
            name=request.form("name"),
            exam_type=request.form["exam_type"],
            duration=request.form["duration"],
            max_marks=request.form["max_marks"],
            slot_creation_start=request.form["slot_start"],
            slot_creation_end=request.form["slot_end"],
            booking_start=request.form["booking_start"],
            booking_end=request.form["booking_end"],
            status=request.form["status"]
        )

        db.session.add(exam)
        db.session.commit()

        flash("exam created successfully", "success")

        return redirect(url_for("view_examination"))

    return render_template("admin/add_examination.html", courses=courses)

@app.route("/admin/examination/edit/<int:id>", methods=["GET", "POST"])
@login_required
def add_examinations(id):
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

        return redirect(url_for("view_examination"))

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

    return redirect(url_for("view_examination"))



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

    return render_template("admin/add_rubric.html", exam=exam)

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
def edit_rubrics(id):
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

    return render_template("admin/examiner", examiners=examiners)


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


@app.route("/examiner/slot/add", methods=["POST", "GET"])
@login_required
def add_slot():
    if current_user.role != 'examiner':
        return redirect(url_for("login"))

    examinations = Examination.query.filter_by(
        examiner_id=current_user.id
    ).all()

    if request.method == "POST":

        examination = Examination.query.get_or_404(request.form["examination"])

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
        capacity = int(request.form["ccapacity"])
        slot = ExaminationSlot(
            examination_id=examination.id,
            examiner_id=current_user.id,
            date=slot_date,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            available_seats=capacity,
            status="Open"
        )

        db.session.add(slot)
        db.sesion.commit()

        flash("Slot created successfully", "success")
        return redirect(url_for("examiner_dashboard"))
    return render_template("examiner/add_slot.html", examinations=examinations)


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
        return redirect(url_for("login"))

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

@app.route("/student/booking/cancel/<int:id>", method=["POST"])
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




with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        from werkzeug.security import generate_password_hash
        admin = User(name='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
        db.session.add(admin)
        db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)
