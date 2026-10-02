from flask import Flask
from models import db, User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Nothing"

db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(email="admin@gmail.com").first():
        admin = User(name='admin', email='admin@gmail.com', password='admin', role='admin')
        db.session.add(admin)
        db.session.commit()
        
if __name__ == "__main__":
    app.run(debug=True)
