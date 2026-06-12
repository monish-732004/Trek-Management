from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Admin, Trek, Booking
from werkzeug.security import check_password_hash
from datetime import datetime

admin = Blueprint("admin", __name__, url_prefix="/admin")

# Helper to verify admin role
def verify_admin():
    if "admin_id" not in session or session.get("role") != "admin":
        return False
    return True

@admin.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query admin from DB
        admin_user = Admin.query.filter_by(username=username).first()

        if not admin_user:
            flash("Username does not exist")
            return redirect(url_for("admin.login"))

        # Verify password (handles plain-text seeded passwords or hashed passwords)
        is_valid = (admin_user.password == password)
        if not is_valid:
            try:
                is_valid = check_password_hash(admin_user.password, password)
            except Exception:
                is_valid = False

        if not is_valid:
            flash("Incorrect password")
            return redirect(url_for("admin.login"))

        # Store session variables
        session["admin_id"] = admin_user.admin_id
        session["role"] = "admin"
        flash("Login Successful")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/admin_login.html")

@admin.route("/dashboard")
def dashboard():
    if not verify_admin():
        flash("Please login first")
        return redirect(url_for("admin.login"))

    return render_template("admin/dashboard.html")

@admin.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("admin.login"))

@admin.route("/treks")
def view_treks():
    if not verify_admin():
        flash("Please login first")
        return redirect(url_for("admin.login"))

    treks = Trek.query.all()
    return render_template("admin/treks.html", treks=treks)

@admin.route("/trek/add", methods=["GET", "POST"])
def add_trek():
    if not verify_admin():
        flash("Please login first")
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        trek_name = request.form.get("trek_name")
        location = request.form.get("location")
        difficulty = request.form.get("difficulty")
        duration_days_str = request.form.get("duration_days")
        available_slots_str = request.form.get("available_slots")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        description = request.form.get("description")
        status = request.form.get("status", "Pending")

        # Parsing numbers
        try:
            duration_days = int(duration_days_str)
            available_slots = int(available_slots_str)
        except (ValueError, TypeError):
            flash("Duration and Available Slots must be valid integers.")
            return redirect(url_for("admin.add_trek"))

        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            flash("Dates must be in YYYY-MM-DD format.")
            return redirect(url_for("admin.add_trek"))

        # Validation checks
        if available_slots <= 0:
            flash("Available slots must be greater than 0.")
            return redirect(url_for("admin.add_trek"))

        if end_date <= start_date:
            flash("End date must be after start date.")
            return redirect(url_for("admin.add_trek"))

        # Save to DB
        try:
            new_trek = Trek(
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
            db.session.add(new_trek)
            db.session.commit()
            flash("Trek created successfully.")
            return redirect(url_for("admin.view_treks"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while creating the trek.")
            print(f"Error creating trek: {e}")
            return redirect(url_for("admin.add_trek"))

    return render_template("admin/add_trek.html")

@admin.route("/trek/edit/<int:trek_id>", methods=["GET", "POST"])
def edit_trek(trek_id):
    if not verify_admin():
        flash("Please login first")
        return redirect(url_for("admin.login"))

    trek = Trek.query.get(trek_id)
    if not trek:
        flash("Trek not found.")
        return redirect(url_for("admin.view_treks"))

    if request.method == "POST":
        trek.trek_name = request.form.get("trek_name")
        trek.location = request.form.get("location")
        trek.difficulty = request.form.get("difficulty")
        duration_days_str = request.form.get("duration_days")
        available_slots_str = request.form.get("available_slots")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        trek.description = request.form.get("description")
        trek.status = request.form.get("status")

        # Parsing numbers
        try:
            trek.duration_days = int(duration_days_str)
            trek.available_slots = int(available_slots_str)
        except (ValueError, TypeError):
            flash("Duration and Available Slots must be valid integers.")
            return redirect(url_for("admin.edit_trek", trek_id=trek_id))

        # Parse dates
        try:
            trek.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            trek.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            flash("Dates must be in YYYY-MM-DD format.")
            return redirect(url_for("admin.edit_trek", trek_id=trek_id))

        # Validation checks
        if trek.available_slots <= 0:
            flash("Available slots must be greater than 0.")
            return redirect(url_for("admin.edit_trek", trek_id=trek_id))

        if trek.end_date <= trek.start_date:
            flash("End date must be after start date.")
            return redirect(url_for("admin.edit_trek", trek_id=trek_id))

        try:
            db.session.commit()
            flash("Trek updated successfully.")
            return redirect(url_for("admin.view_treks"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the trek.")
            print(f"Error editing trek: {e}")
            return redirect(url_for("admin.edit_trek", trek_id=trek_id))

    return render_template("admin/edit_trek.html", trek=trek)

@admin.route("/trek/delete/<int:trek_id>", methods=["POST"])
def delete_trek(trek_id):
    if not verify_admin():
        flash("Please login first")
        return redirect(url_for("admin.login"))

    trek = Trek.query.get(trek_id)
    if not trek:
        flash("Trek not found.")
        return redirect(url_for("admin.view_treks"))

    # Check whether bookings exist
    has_bookings = Booking.query.filter_by(trek_id=trek_id).first() is not None
    if has_bookings:
        flash(f"Cannot delete trek '{trek.trek_name}' because bookings exist.")
        return redirect(url_for("admin.view_treks"))

    try:
        db.session.delete(trek)
        db.session.commit()
        flash("Trek deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the trek.")
        print(f"Error deleting trek: {e}")

    return redirect(url_for("admin.view_treks"))