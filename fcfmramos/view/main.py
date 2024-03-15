from flask import Blueprint
from flask import render_template, redirect, url_for, request

from fcfmramos.view.auth import is_logged_in
from fcfmramos.model import db
from fcfmramos.model.ucampus import Ramo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    page = request.args.get('page', 1, type=int)

    #ramos = db.session.execute(db.select(Ramo)).scalars()
    ramos = db.paginate(db.select(Ramo), page=page, per_page=20)

    return render_template(
        "index.html",
        ramos=ramos,
        serialized_ramos=[ramo.serialize() for ramo in ramos.items]
    )


@bp.route("/profile")
def profile():
    if not is_logged_in():
        return redirect(url_for("auth.login"))

    return render_template("profile.html")
