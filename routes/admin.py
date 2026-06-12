from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Admin
from werkzeug.security import check_password_hash

admin = Blueprint("admin", __name__, url_prefix="/admin")

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
    # Authorization check
    if "admin_id" not in session or session.get("role") != "admin":
        flash("Please login first")
        return redirect(url_for("admin.login"))

    return render_template("admin/dashboard.html")

@admin.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("admin.login"))