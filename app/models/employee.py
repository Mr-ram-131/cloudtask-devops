from datetime import datetime

from app import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False
    )

    joining_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow 
    )

    tasks = db.relationship(
        "Task",
        backref="employee",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Employee {self.name}>"