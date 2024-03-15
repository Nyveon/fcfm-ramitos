from flask import Blueprint
from flask import render_template, redirect, url_for, request
from sqlalchemy import or_

from fcfmramos.view.auth import is_logged_in
from fcfmramos.model import db
from fcfmramos.model.ucampus import Ramo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')

    #ramos = db.session.execute(db.select(Ramo)).scalars()
    query = db.select(Ramo)
    if search_query:
        query = query.where(or_(
            Ramo.nombre.ilike(f"%{search_query}%"),
            Ramo.codigo.ilike(f"%{search_query}%")
        ))
    ramos = db.paginate(query, page=page, per_page=20)

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
