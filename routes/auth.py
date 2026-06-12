from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import db, User
from werkzeug.security import check_password_hash
from models import db, User, Trek
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

auth = Blueprint("auth", __name__)

@auth.route("/register/user", methods=["GET", "POST"])
def register_user():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        emergency_contact = request.form["emergency_contact"]
        age_input = request.form["age"]
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).one_or_none()

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("auth.register_user"))

        # Password Validation
        if (
            len(password) < 8
            or not any(char.isupper() for char in password)
            or not any(char.isdigit() for char in password)
            or not any(not char.isalnum() for char in password)
        ):
            flash(
                "Password must be at least 8 characters long and contain at least one uppercase letter, one number, and one special character."
            )
            return redirect(url_for("auth.register_user"))

        # Age handling
        if age_input:
            age = int(age_input)
        else:
            age = None

        # Hash password
        hashed_password = generate_password_hash(password)

        # Create user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone,
            age=age,
            emergency_contact=emergency_contact
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Welcome aboard! Your journey starts here")
        return redirect(url_for("auth.login"))

    return render_template("auth/user_register.html")

from werkzeug.security import check_password_hash

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            flash("User havent registered yet!! Register Please")
            return redirect(
                url_for("auth.login")
            )

        if user.status == "Blacklisted":
            flash("Your account has been blacklisted")
            return redirect(
                url_for("auth.login")
            )

        if not check_password_hash(
            user.password,
            password
        ):
            flash(" Wrong password")
            return redirect(
                url_for("auth.login")
            )

        session["user_id"] = user.user_id
        session["user_name"] = user.name
        session["role"] = "user"

        flash("Login Successful")

        treks = Trek.query.filter_by(
            status="Open"
        ).all()

        return render_template(
            "user/dashboard.html",
            name=user.name,
            treks=treks
        )

    return render_template(
        "auth/login.html"
    )

@auth.route("/dashboard")
def user_dashboard():

    if "user_id" not in session:

        flash("Please login first")

        return redirect(
            url_for("auth.login")
        )

    treks = Trek.query.filter_by(
        status="Open"
    ).all()

    return render_template(
        "user/dashboard.html",
        name=session["user_name"],
        treks=treks
    )
@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully")

    return redirect(
        url_for("auth.login")
    )