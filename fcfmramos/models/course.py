from fcfmramos import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(128), unique=True, nullable=False)
    department = db.Column(
        db.Integer, db.ForeignKey("department.id"), nullable=False
    )


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    code = db.Column(db.String(128), unique=True, nullable=False)
    color = db.Column(db.String(6), nullable=False)
