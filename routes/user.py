from flask import Blueprint, redirect, url_for, flash, session, render_template
from models import db, Trek, Booking, User

user = Blueprint("user", __name__)

@user.route("/my-bookings")
def my_bookings():
    if "user_id" not in session or session.get("role") != "user":
        flash("Please login first.")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    bookings = (
        Booking.query
        .filter_by(user_id=user_id)
        .order_by(Booking.booking_date.desc())
        .all()
    )
    return render_template("user/my_bookings.html", bookings=bookings)

@user.route("/book/<int:trek_id>")
def book_trek(trek_id):
    # Verify user is logged in
    if "user_id" not in session or session.get("role") != "user":
        flash("Please login first")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    # Query the trek and check if it exists
    trek = Trek.query.get(trek_id)
    if not trek:
        flash("Trek not found.")
        return redirect(url_for("auth.user_dashboard"))

    # Check that trek status is "Open"
    if trek.status != "Open":
        flash(f"Trek '{trek.trek_name}' is not open for bookings.")
        return redirect(url_for("auth.user_dashboard"))

    # Check available slots > 0
    if trek.available_slots is None or trek.available_slots <= 0:
        flash(f"Sorry, no available slots for '{trek.trek_name}'.")
        return redirect(url_for("auth.user_dashboard"))

    # Check user has not already booked this trek
    existing_booking = Booking.query.filter_by(user_id=user_id, trek_id=trek_id).first()
    if existing_booking:
        flash(f"You have already booked the trek '{trek.trek_name}'!")
        return redirect(url_for("auth.user_dashboard"))

    # Create booking and reduce slots
    try:
        new_booking = Booking(
            user_id=user_id,
            trek_id=trek_id,
            status="Booked"
        )
        db.session.add(new_booking)

        trek.available_slots -= 1
        db.session.commit()
        flash("Trek booked successfully.")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while booking. Please try again.")
        print(f"Error booking trek: {e}")

    return redirect(url_for("auth.user_dashboard"))

@user.route("/trek/<int:trek_id>")
def trek_detail(trek_id):
    if "user_id" not in session or session.get("role") != "user":
        flash("Please login first.")
        return redirect(url_for("auth.login"))

    trek = Trek.query.get(trek_id)
    if not trek:
        flash("Trek not found.")
        return redirect(url_for("auth.user_dashboard"))

    return render_template("user/trek_detail.html", trek=trek)

