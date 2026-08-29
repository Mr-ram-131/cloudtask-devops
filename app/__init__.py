from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.employees import employees
    app.register_blueprint(employees)

    from app.routes.tasks import tasks
    app.register_blueprint(tasks)

    from app.models import User, Employee, Task

    return app