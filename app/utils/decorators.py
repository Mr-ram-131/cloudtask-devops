from functools import wraps

from flask import session, redirect, url_for, flash


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return function(*args, **kwargs)

    return wrapper


def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        if session.get("role") != "admin":

            flash(
                "You do not have permission to access this page.",
                "error"
            )

            return redirect(
                url_for("main.dashboard")
            )

        return function(*args, **kwargs)

    return wrapper