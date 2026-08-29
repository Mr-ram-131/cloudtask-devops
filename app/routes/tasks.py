from datetime import datetime
from app.utils.decorators import admin_required, login_required

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
from app.models.task import Task
from app.models.employee import Employee


tasks = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


@tasks.route("/")
@admin_required
def task_list():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    all_tasks = Task.query.order_by(
        Task.id.desc()
    ).all()

    return render_template(
        "tasks.html",
        tasks=all_tasks
    )


@tasks.route("/add", methods=["GET", "POST"])
@admin_required
def add_task():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    employees = Employee.query.order_by(
        Employee.name
    ).all()

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        employee_id = request.form.get("employee_id")
        priority = request.form.get("priority")
        status = request.form.get("status")
        due_date = request.form.get("due_date")

        if not title or not employee_id:
            flash(
                "Title and employee are required.",
                "error"
            )

            return redirect(
                url_for("tasks.add_task")
            )

        employee = Employee.query.get(
            int(employee_id)
        )

        if not employee:
            flash(
                "Selected employee does not exist.",
                "error"
            )

            return redirect(
                url_for("tasks.add_task")
            )

        task = Task(
            title=title,
            description=description,
            employee_id=int(employee_id),
            priority=priority,
            status=status
        )

        if due_date:
            task.due_date = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()

        db.session.add(task)
        db.session.commit()

        flash(
            "Task created successfully.",
            "success"
        )

        return redirect(
            url_for("tasks.task_list")
        )

    return render_template(
        "add_task.html",
        employees=employees
    )


@tasks.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_task(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(id)

    employees = Employee.query.order_by(
        Employee.name
    ).all()

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        employee_id = request.form.get("employee_id")
        priority = request.form.get("priority")
        status = request.form.get("status")
        due_date = request.form.get("due_date")

        task.title = title
        task.description = description
        task.employee_id = int(employee_id)
        task.priority = priority
        task.status = status

        if due_date:
            task.due_date = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            ).date()
        else:
            task.due_date = None

        db.session.commit()

        flash(
            "Task updated successfully.",
            "success"
        )

        return redirect(
            url_for("tasks.task_list")
        )

    return render_template(
        "edit_task.html",
        task=task,
        employees=employees
    )


@tasks.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_task(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    flash(
        "Task deleted successfully.",
        "success"
    )

    return redirect(
        url_for("tasks.task_list")
    )

@tasks.route("/my-tasks")
@login_required
def my_tasks():

    user_id = session.get("user_id")

    employee = Employee.query.filter_by(
        user_id=user_id
    ).first()

    if not employee:
        flash(
            "No employee profile is linked to your account.",
            "error"
        )

        return redirect(
            url_for("main.dashboard")
        )

    my_task_list = Task.query.filter_by(
        employee_id=employee.id
    ).order_by(
        Task.id.desc()
    ).all()

    return render_template(
        "my_tasks.html",
        tasks=my_task_list,
        employee=employee
    )