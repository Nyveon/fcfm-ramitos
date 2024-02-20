from flask import Blueprint
from flask import render_template, redirect, url_for

from fcfmramos.view.auth import is_logged_in

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    return render_template("profile.html")
