from flask import Blueprint
from flask import render_template, redirect, url_for

from fcfmramos.view.auth import is_logged_in
from fcfmramos.model import db
from fcfmramos.model.course import Curso

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # get all courses from database sqlalchemy

    courses = db.session.query(Curso).all()

    return render_template("index.html", courses=courses)


@bp.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    return render_template("profile.html")
