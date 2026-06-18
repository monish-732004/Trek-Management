from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Admin
class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(200), unique=True)

    def __init__(self, username=None, password=None, email=None):
        super().__init__(
            username=username,
            password=password,
            email=email
        )


# User
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
    created_at = db.Column(db.DateTime, default=datetime.now)
    bookings = db.relationship("Booking", back_populates="user", lazy=True)
    reviews = db.relationship("Review", back_populates="user", lazy=True)

    def __init__(self, name=None, email=None, password=None, phone=None, age=None, emergency_contact=None, status="Active", created_at=None):
        super().__init__(
            name=name,
            email=email,
            password=password,
            phone=phone,
            age=age,
            emergency_contact=emergency_contact,
            status=status,
            created_at=created_at
        )


# Staff
class Staff(db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    contact = db.Column(db.String(20))
    experience = db.Column(db.Integer)
    status = db.Column(db.String(30), default="Active")

    def __init__(self, name=None, email=None, password=None, contact=None, experience=None, status="Active"):
        super().__init__(
            name=name,
            email=email,
            password=password,
            contact=contact,
            experience=experience,
            status=status
        )


# Trek
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
    bookings = db.relationship("Booking", back_populates="trek", lazy=True)
    reviews = db.relationship("Review", back_populates="trek", lazy=True)

    def __init__(self, trek_name=None, location=None, difficulty=None, duration_days=None, available_slots=None, start_date=None, end_date=None, description=None, status="Pending"):
        super().__init__(
            trek_name=trek_name,
            location=location,
            difficulty=difficulty,
            duration_days=duration_days,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date,
            description=description,
            status=status
        )


# TrekAssignment
class TrekAssignment(db.Model):
    __tablename__ = "trek_assignments"
    assignment_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, staff_id=None, trek_id=None, assigned_date=None):
        super().__init__(
            staff_id=staff_id,
            trek_id=trek_id,
            assigned_date=assigned_date
        )


# Booking
class Booking(db.Model):
    __tablename__ = "bookings"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default="Booked")
    user = db.relationship("User", back_populates="bookings")
    trek = db.relationship("Trek", back_populates="bookings")

    def __init__(self, user_id=None, trek_id=None, booking_date=None, status="Booked"):
        super().__init__(
            user_id=user_id,
            trek_id=trek_id,
            booking_date=booking_date,
            status=status
        )


# Review
class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship("User", back_populates="reviews")
    trek = db.relationship("Trek", back_populates="reviews")

    def __init__(self, user_id=None, trek_id=None, rating=None, comment=None, review_date=None):
        super().__init__(
            user_id=user_id,
            trek_id=trek_id,
            rating=rating,
            comment=comment,
            review_date=review_date
        )