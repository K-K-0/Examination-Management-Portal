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
            code=request.form("code")
            name=request.form("name")
            description=request.form("description")
            status=request.form("status")
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
        
        course.code=request.form("code")
        course.name=request.form("name")
        course.description=request.form("description")
        course.status=request.form("status")

        db.session.commit()

        flash("course updated successfully", "success")
        return redirect(url_for("view_courses"))

    return render_template("admin/edit_course.html", course=course)























with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        from werkzeug.security import generate_password_hash
        admin = User(name='admin', email='admin@gmail.com', password=generate_password_hash('admin'), role='admin')
        db.session.add(admin)
        db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)
