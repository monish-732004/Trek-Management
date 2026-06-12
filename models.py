from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
#Admin
class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(200), unique=True)
#user
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(14))
    age = db.Column(db.Integer)
    emergency_contact = db.Column(db.String(16))
    status = db.Column(db.String(30), default="Active")
    created_at = db.Column(db.DateTime,default=datetime.now)
    bookings = db.relationship("Booking",back_populates="user",lazy=True)
    reviews = db.relationship("Review",back_populates="user",lazy=True)
#Staff
class Staff(db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    contact = db.Column(db.String(20))
    experience = db.Column(db.Integer)
    status = db.Column(db.String(30), default="Active")
#Trek
class Trek(db.Model):
    __tablename__ = "treks"
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    difficulty = db.Column(db.String(30))
    duration_days = db.Column(db.Integer)
    available_slots = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="Pending")
    bookings = db.relationship("Booking",back_populates="trek",lazy=True)
    reviews = db.relationship("Review",back_populates="trek",lazy=True)
#Trek
class TrekAssignment(db.Model):
    __tablename__ = "trek_assignments"
    assignment_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer,db.ForeignKey("staff.staff_id"),nullable=False)
    trek_id = db.Column(db.Integer,db.ForeignKey("treks.trek_id"),nullable=False)
    assigned_date = db.Column(db.DateTime,default=datetime.now)
#Booking
class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    trek_id = db.Column(db.Integer,db.ForeignKey("treks.trek_id"),nullable=False)
    booking_date = db.Column(db.DateTime,default=datetime.now)
    status = db.Column(db.String(20),default="Booked")
    user = db.relationship("User",back_populates="bookings")
    trek = db.relationship("Trek",back_populates="bookings")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
#Review
class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    trek_id = db.Column(db.Integer,db.ForeignKey("treks.trek_id"),nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime,default=datetime.now)
    user = db.relationship("User", back_populates="reviews")
    trek = db.relationship("Trek",back_populates="reviews")