from app.utils.decorators import admin_required
from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from app import db
from app.models.employee import Employee


employees = Blueprint("employees", __name__, url_prefix="/employees")


def login_required():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return None


@employees.route("/")
@admin_required
def employee_list():

  

    all_employees = Employee.query.order_by(
        Employee.id.desc()
    ).all()

    return render_template(
        "employees.html",
        employees=all_employees
    )


@employees.route("/add", methods=["GET", "POST"])
@admin_required
def add_employee():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        role = request.form.get("role")
        joining_date = request.form.get("joining_date")

        if not name or not email or not department or not role or not joining_date:
            flash("All fields are required.", "error")
            return redirect(url_for("employees.add_employee"))

        existing_employee = Employee.query.filter_by(
            email=email
        ).first()

        if existing_employee:
            flash("An employee with this email already exists.", "error")
            return redirect(url_for("employees.add_employee"))

        employee = Employee(
            name=name,
            email=email,
            department=department,
            role=role,
            joining_date=datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date()
        )

        db.session.add(employee)
        db.session.commit()

        flash("Employee added successfully.", "success")

        return redirect(url_for("employees.employee_list"))

    return render_template("add_employee.html")


@employees.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_employee(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        department = request.form.get("department")
        role = request.form.get("role")
        joining_date = request.form.get("joining_date")

        existing_employee = Employee.query.filter(
            Employee.email == email,
            Employee.id != id
        ).first()

        if existing_employee:
            flash("Another employee already uses this email.", "error")
            return redirect(
                url_for(
                    "employees.edit_employee",
                    id=id
                )
            )

        employee.name = name
        employee.email = email
        employee.department = department
        employee.role = role

        if joining_date:
            employee.joining_date = datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date()

        db.session.commit()

        flash("Employee updated successfully.", "success")

        return redirect(
            url_for("employees.employee_list")
        )

    return render_template(
        "edit_employee.html",
        employee=employee
    )


@employees.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_employee(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    flash("Employee deleted successfully.", "success")

    return redirect(
        url_for("employees.employee_list")
    )