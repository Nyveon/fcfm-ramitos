import json

from functools import wraps

from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length

import pyrebase

import config


app = Flask(__name__)
app.secret_key = config.secret_key

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)

firebase = pyrebase.initialize_app(json.load(open("fbconfig.json")))
auth = firebase.auth()


class LoginForm(FlaskForm):
    email = StringField(
        "Correo (@ug.uchile.cl)", validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=8)]
    )
    submit = SubmitField("Ingresar")


def validate_email_domain(form, field):
    if not field.data.endswith("@ug.uchile.cl"):
        print("this")
        raise ValidationError("El correo debe terminar en @ug.uchile.cl")


class SignupForm(FlaskForm):
    email = StringField(
        "Correo (@ug.uchile.cl)",
        validators=[DataRequired(), Email(), validate_email_domain],
    )
    password = PasswordField(
        "Contraseña", validators=[DataRequired(), Length(min=8)]
    )
    submit = SubmitField("Crear cuenta")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session)
        if "user" not in session:
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return wrap


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/userinfo")
@login_required
def userinfo():
    return {"data": "gaming"}


def login_email_password(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    session["user"] = user["idToken"]


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()

    if "user" in session:
        return {"message": "Ya estás ingresadx"}, 200

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            auth.create_user_with_email_and_password(email, password)
            login_email_password(email, password)
            return {"message": "Successfully created user"}, 200
        except Exception as e:
            print(e)
            return {"message": "Error creating user"}, 400

    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if "user" in session:
        return {"message": "Ya estás ingresadx"}, 200

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            login_email_password(email, password)
            return {"message": "Login successful"}, 200
        except Exception as e:
            print(e)
            return {"message": "Login failed"}, 400

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

# user = auth.sign_in_with_email_and_password(email, password)
# auth.get_account_info(user['idToken'])
# auth.send_email_verificaction(user['idToken'])
# auth.send_password_reset_email(email)
