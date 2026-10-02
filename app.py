from flask import Flask
from models import db, User, Booking, Course, Examination, ExaminationSlot, Rubric
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager , login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Nothing"

db.init_app(app)
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = "login"


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








with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        from werkzeug.security import generate_password_hash
        admin = User(name='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
        db.session.add(admin)
        db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)
