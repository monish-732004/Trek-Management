from flask import Flask, render_template
from models import db, Admin
from routes.auth import auth


app = Flask(__name__)

app.secret_key = "trekking_secret_key_2026"
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

app.register_blueprint(auth)


if __name__ == "__main__":
    app.run(debug=True)