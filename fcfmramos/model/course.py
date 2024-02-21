from dataclasses import dataclass

from fcfmramos.model import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ucampus_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(128), unique=True, nullable=False)
    color = db.Column(db.String(6), nullable=True)


@dataclass
class Course(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(128), nullable=False)
    code: str = db.Column(db.String(128), unique=True, nullable=False)
    department: int = db.Column(
        db.Integer, db.ForeignKey("department.id"), nullable=False
    )
    sct: int = db.Column(db.Integer, nullable=False)
    requisitos: str = db.Column(db.String(128), nullable=False)
