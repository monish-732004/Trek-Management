from flask import Flask, render_template
from models import db, Admin, Trek
from routes.auth import auth
from routes.user import user

app = Flask(__name__)

app.secret_key = "trekking_secret_key_2026"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekkingmanagement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

    default_admin = Admin.query.filter_by(
        username="Admin"
    ).first()

    if not default_admin:
        default_admin = Admin(username="Admin",password="Admin@123",email="adminspeaks@trek.com")
        db.session.add(default_admin)
        db.session.commit()

    trek = Trek.query.first()

    if not trek:

        trek1 = Trek(
            trek_name="Kedarkantha",
            location="Uttarakhand",
            difficulty="Moderate",
            duration_days=5,
            available_slots=20,
            status="Open"
        )

        trek2 = Trek(
            trek_name="Rajmachi",
            location="Maharashtra",
            difficulty="Easy",
            duration_days=2,
            available_slots=15,
            status="Open"
        )

        db.session.add(trek1)
        db.session.add(trek2)
        db.session.commit()

print("Database created successfully!")

app.register_blueprint(auth)
app.register_blueprint(user)


if __name__ == "__main__":
    app.run(debug=True)