from flask import Blueprint, jsonify
from flask import render_template

from fcfmramos.model import db
from fcfmramos.model.ucampus import Plan, Subplan

bp = Blueprint("catalog", __name__)


@bp.route("/subplan/<int:subplan_id>")
def subplan(subplan_id: int):
    subplan = db.session.query(Subplan).get(subplan_id) # todo: outdate sqlalchemy syntax
    if subplan is None:
        return jsonify({"error": "Subplan not found"}), 404

    ramos = []
    for ramo in subplan.ramos:
        ramos.append(ramo.serialize())

    for child in subplan.child_subplanes:
        if child.absorb:
            print(child.nombre)
            for ramo in child.ramos:
                ramos.append(ramo.serialize())

    print(ramos)

    print(subplan.nickname)

    return render_template(
        "catalog.html",
        courses=ramos,
        subplans=subplan.child_subplanes,
        plan=subplan.plan,
        subplan=subplan,
    )


@bp.route("/<string:plan_id>")
def plan(plan_id: str):
    carrera_id, version = plan_id.split("_")

    # find plan in database
    plan = (
        db.session.query(Plan)
        .filter_by(carrera=carrera_id, version=version)
        .first()
    ) # todo: outdate sqlalchemy syntax

    subplans = plan.subplanes
    first_layer = [subplan for subplan in subplans[0].child_subplanes]
    x = " ".join([subplan.nombre for subplan in first_layer])
    x += "|||||||||||||||||"
    for subplan in first_layer:
        x += " ".join([subplan.nombre for subplan in subplan.child_subplanes])

    return f"Plan {plan.nombre} {x}"


def serialize_subplan(subplan):
    """Recursively serialize a Subplan including its child subplans."""
    return {
        "id": subplan.id,
        "nombre": subplan.nombre,
        "child_subplanes": [
            serialize_subplan(child) for child in subplan.child_subplanes
        ],
    }


@bp.route("/plans/<string:plan_id>/subplans/tree")
def get_subplan_tree(plan_id: str):
    carrera_id, version = plan_id.split("_")

    plan = (
        db.session.query(Plan)
        .filter_by(carrera=carrera_id, version=version)
        .first()
    ) # todo: outdate sqlalchemy syntax
    if plan is None:
        return jsonify({"error": "Plan not found"}), 404

    top_level_subplans = [
        subplan for subplan in plan.subplanes if subplan.parent_subplan is None
    ]

    subplans_tree = [
        serialize_subplan(subplan) for subplan in top_level_subplans
    ]

    return jsonify(subplans_tree)
