from flask import Blueprint
from flask import render_template, redirect, url_for

from fcfmramos.view.auth import is_logged_in
from fcfmramos.model import db
from fcfmramos.model.ucampus import Ramo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # get all courses from database sqlalchemy

    ramos = db.session.query(Ramo).all()

    return render_template(
        "index.html", courses=[ramo.serialize() for ramo in ramos]
    )


@bp.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    return render_template("profile.html")
