from flask import Flask
from models import db, Admin

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekkingmanagement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

    admin = Admin.query.filter_by(
        username="Admin"
    ).first()

    if not admin:
        admin = Admin(username="Admin",password="Admin@123",email="adminspeaks@trek.com")
        db.session.add(admin)
        db.session.commit()

print("Database created successfully!")