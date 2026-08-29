from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session, flash


from app import db, bcrypt
from app.models.user import User
from app.models.employee import Employee


auth = Blueprint("auth", __name__)




@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        department = request.form.get("department")
        job_role = request.form.get("job_role")

        if not username or not email or not password or not department or not job_role:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "error")
            return redirect(url_for("auth.register"))

        existing_employee = Employee.query.filter_by(email=email).first()

        if existing_employee:
            flash("An employee with this email already exists.", "error")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user_count = User.query.count()

        if user_count == 0:
            user_role = "admin"
        else:
            user_role = "employee"


        user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=user_role
        )

        db.session.add(user)
        db.session.flush()

        if user_role == "employee":

            employee = Employee(
                user_id=user.id,
                name=username,
                email=email,
                department=department,
                role=job_role,
                joining_date=datetime.utcnow().date()
            )

            db.session.add(employee)

        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))