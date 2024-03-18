import asyncio
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from fcfmramos.web_scraper.main import scrape_catalogos, scrape_planes
from fcfmramos.model.ucampus import (
    Departamento,
    Ramo,
    Curso,
    Profesor,
    Plan,
    Subplan,
)


def populate_catalogos(db: SQLAlchemy) -> None:
    catalogos = asyncio.run(scrape_catalogos())

    for catalogo in catalogos:
        semestre_full = str(catalogo.semestre)
        print(f"Saving: D{catalogo.departamento.id}S{semestre_full}")
        year = semestre_full[:4]
        semester = semestre_full[4]

        department = Departamento.query.filter_by(
            ucampus_id=catalogo.departamento.id
        ).first()

        if not department:
            department = Departamento(
                ucampus_id=catalogo.departamento.id,
                nombre=catalogo.departamento.nombre,
                codigo=catalogo.departamento.codigo,
                color=catalogo.departamento.color,
            )
            db.session.add(department)

        for ramo in catalogo.ramos:
            ramo_object = Ramo.query.filter_by(codigo=ramo.codigo).first()
            if not ramo_object:
                ramo_object = Ramo(
                    nombre=ramo.nombre,
                    codigo=ramo.codigo,
                    sct=ramo.sct,
                    departamento_id=department.id,
                    requisitos=ramo.requisitos,
                    sustentabilidad=ramo.sustentabilidad,
                )
                db.session.add(ramo_object)

            for curso in ramo.secciones:
                curso_object = Curso.query.filter_by(
                    año=year,
                    semestre=semester,
                    seccion=curso.seccion,
                    ramo_id=ramo_object.id,
                ).first()

                if not curso_object:
                    curso_object = Curso(
                        año=year,
                        semestre=semester,
                        seccion=curso.seccion,
                        ramo_id=ramo_object.id,
                        cupos=curso.cupos,
                        cupos_ocupados=curso.cupos_ocupados,
                    )
                    db.session.add(curso_object)

                for profe in curso.profesores:
                    profesor = Profesor.query.filter_by(
                        ucampus_id=profe.ucampus_id
                    ).first()
                    if not profesor:
                        profesor = Profesor(
                            nombre=profe.nombre, ucampus_id=profe.ucampus_id
                        )
                        db.session.add(profesor)

                    if profesor not in curso_object.profesores:
                        curso_object.profesores.append(profesor)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def populate_planes(db: SQLAlchemy) -> None:
    scraped_data = asyncio.run(scrape_planes())

    for plan_data in scraped_data:
        plan = insert_or_update_plan(db, plan_data)
        for subplan_data in plan_data.subplanes:
            insert_or_update_subplan(db, subplan_data, plan)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def insert_or_update_plan(db: SQLAlchemy, plan_data) -> None:
    plan = (
        db.session.query(Plan)
        .filter_by(carrera=plan_data.carr_codigo, version=plan_data.c_plan)
        .first()
    )

    department = Departamento.query.filter_by(
        ucampus_id=plan_data.departamento_id
    ).first()

    if not plan:
        plan = Plan(
            nombre=plan_data.nombre,
            carrera=plan_data.carr_codigo,
            version=plan_data.c_plan,
            departamento_id=department.id,
        )
        db.session.add(plan)

    db.session.commit()
    return plan


def insert_or_update_subplan(
    db: SQLAlchemy, subplan_data, parent_plan, parent_subplan=None
):
    subplan = (
        db.session.query(Subplan)
        .filter_by(nombre=subplan_data.subplan_name, plan=parent_plan)
        .first()
    )
    if not subplan:
        subplan = Subplan(
            nombre=subplan_data.subplan_name,
            plan=parent_plan,
            parent_subplan=parent_subplan,
        )
        db.session.add(subplan)
    db.session.commit()
    for child_subplan_data in subplan_data.subplanes:
        insert_or_update_subplan(db, child_subplan_data, parent_plan, subplan)
    for ramo_data in subplan_data.ramos:
        insert_or_update_ramo(db, ramo_data, subplan)
    return subplan


def insert_or_update_ramo(db: SQLAlchemy, ramo_data, parent_subplan):
    ramo = db.session.query(Ramo).filter_by(codigo=ramo_data.codigo).first()
    if not ramo:
        return

    if ramo not in parent_subplan.ramos:
        parent_subplan.ramos.append(ramo)
    db.session.commit()
