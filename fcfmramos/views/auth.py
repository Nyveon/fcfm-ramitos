import json

from functools import wraps

from flask import session, redirect, flash, url_for, render_template
from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length

import pyrebase

bp = Blueprint("auth", __name__)


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


class RecoverPasswordForm(FlaskForm):
    email = StringField(
        "Correo (@ug.uchile.cl)",
        validators=[DataRequired(), Email(), validate_email_domain],
    )
    submit = SubmitField("Recuperar contraseña")


def is_logged_in():
    # Is email verified
    return "user" in session


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not is_logged_in():
            return {"message": "Unauthorized"}, 401
        return f(*args, **kwargs)

    return wrap


def is_verified():
    if not is_logged_in():
        return False
    return auth.get_account_info(session["user"])["users"][0]["emailVerified"]


def login_email_password(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    session["user"] = user["idToken"]
    session["username"] = email.split("@")[0]


@bp.route("/signup", methods=["POST", "GET"])
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

            try:
                auth.send_email_verification(session["user"])
            except Exception as e:
                print(e)
                flash(
                    "Error en envío de correo, por favor contactar al admin",
                    "error",
                )
                return redirect(url_for("main.index"))

            flash("Cuenta creada", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            print(e)
            flash("Error en creación de cuenta", "error")
            return redirect(url_for("signup"))

    return render_template("signup.html", form=form)


@bp.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    form = RecoverPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        try:
            auth.send_password_reset_email(email)
            flash("Correo de recuperación enviado a tu correo", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            print(e)
            flash("Error en envío de correo de recuperación", "error")
            return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html", form=form)


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if "user" in session:
        return {"message": "Ya estás ingresadx"}, 200

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            login_email_password(email, password)

            flash("Ingreso exitoso", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            print(e)
            flash("Error en inicio de sesión", "error")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("main.index"))