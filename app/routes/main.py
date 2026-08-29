from flask import Blueprint, render_template, session, redirect, url_for

from app import db


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/db-test")
def db_test():
    try:
        db.session.execute(db.text("SELECT 1"))
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"


@main.route("/create-tables")
def create_tables():
    from app.models import User, Employee, Task

    db.create_all()

    return "Database tables created successfully!"

@main.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    from app.models.employee import Employee
    from app.models.task import Task

    role = session.get("role")
    username = session.get("username")

    if role == "admin":

        total_employees = Employee.query.count()
        total_tasks = Task.query.count()

        pending_tasks = Task.query.filter_by(status="Pending").count()
        completed_tasks = Task.query.filter_by(status="Completed").count()
        in_progress_tasks = Task.query.filter_by(status="In Progress").count()

        return render_template(
            "dashboard.html",
            username=username,
            role=role,
            total_employees=total_employees,
            total_tasks=total_tasks,
            pending_tasks=pending_tasks,
            completed_tasks=completed_tasks,
            in_progress_tasks=in_progress_tasks
        )

    # Employee dashboard: only their own task summary.
    employee = Employee.query.filter_by(
        user_id=session.get("user_id")
    ).first()

    if not employee:
        return render_template(
            "dashboard.html",
            username=username,
            role=role,
            employee=None
        )

    my_tasks = Task.query.filter_by(employee_id=employee.id).all()

    total_tasks = len(my_tasks)
    pending_tasks = len([t for t in my_tasks if t.status == "Pending"])
    in_progress_tasks = len([t for t in my_tasks if t.status == "In Progress"])
    completed_tasks = len([t for t in my_tasks if t.status == "Completed"])

    return render_template(
        "dashboard.html",
        username=username,
        role=role,
        employee=employee,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        in_progress_tasks=in_progress_tasks
    )