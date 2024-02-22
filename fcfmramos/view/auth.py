import json

from functools import wraps

from flask import session, redirect, flash, url_for, render_template
from flask import Blueprint

import pyrebase  # type: ignore

from fcfmramos.model import db
from fcfmramos.model.user import User
from fcfmramos.view.forms.accounts import (
    LoginForm,
    SignupForm,
    RecoverPasswordForm,
)

bp = Blueprint("auth", __name__)


firebase = pyrebase.initialize_app(json.load(open("fbconfig.json")))
auth = firebase.auth()


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

    user_id = session["user"]
    user_token = session["user_token"]
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        print("Ghost user, wth?")

    if user.email_verified:
        return True

    try:
        verified_check = auth.get_account_info(user_token)["users"][0][
            "emailVerified"
        ]
        if verified_check:
            print(f"User: {user_id} now verified")
            user.email_verified = True
            db.session.commit()
        return verified_check
    except Exception as e:
        print(f"Error checking email verification: {e}")
        return False


def login_email_password(email, password):
    user = auth.sign_in_with_email_and_password(email, password)
    session["user_token"] = user["idToken"]
    session["user"] = user["localId"]

    local_user = User.query.filter_by(id=session["user"]).first()
    if local_user is None:
        new_user = User(
            id=session["user"],
            email=email,
            username=email.split("@")[0],
            email_verified=False,
        )
        db.session.add(new_user)
        db.session.commit()


@bp.route("/verify_email", methods=["GET"])
def send_verification_email():
    print(session)

    if not is_logged_in():
        return {"message": "Unauthorized"}, 401

    try:
        auth.send_email_verification(session["user_token"])
        flash("Correo de verificación enviado", "success")
        return redirect(url_for("main.index"))
    except Exception as e:
        print(f"Error sending email verification: {e}")
        flash("Error en envío de correo de verificación", "error")
        return redirect(url_for("main.index"))


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()

    if "user" in session:
        return {"message": "Ya estás ingresadx"}, 200

    if form.validate_on_submit():
        email = form.email.data
        # todo: if no @, insert @ug.uchile.cl
        password = form.password.data

        try:
            auth.create_user_with_email_and_password(email, password)
            login_email_password(email, password)

            try:
                auth.send_email_verification(session["user_token"])
            except Exception as e:
                print(f"Error sending email verification: {e}")
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
            return redirect(url_for("auth.signup"))

    return render_template("auth/signup.html", form=form)


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
            return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html", form=form)


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if is_logged_in():
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
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("main.index"))
