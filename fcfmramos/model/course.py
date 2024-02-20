from fcfmramos.model import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ucampus_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(128), unique=True, nullable=False)
    color = db.Column(db.String(6), nullable=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(128), unique=True, nullable=False)
    department = db.Column(
        db.Integer, db.ForeignKey("department.id"), nullable=False
    )
    sct = db.Column(db.Integer, nullable=False)
    requisitos = db.Column(db.String(128), nullable=False)
