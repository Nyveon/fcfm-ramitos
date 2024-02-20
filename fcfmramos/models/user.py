from fcfmramos import db


class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
