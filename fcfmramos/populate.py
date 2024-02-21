import asyncio
from flask_sqlalchemy import SQLAlchemy

from fcfmramos.web_scraper.main import main
from fcfmramos.model.course import (
    Course,
    Section,
    Professor,
    SectionProfessor,
    Department,
)


def populate(db: SQLAlchemy):
    catalogos = asyncio.run(main())

    for catalogo in catalogos:
        department = Department.query.filter_by(
            ucampus_id=catalogo.departamento.id
        ).first()
        if not department:
            department = Department(
                ucampus_id=catalogo.departamento.id,
                name=catalogo.departamento.nombre,
                code=catalogo.departamento.codigo,
                color=catalogo.departamento.color,
            )
            db.session.add(department)
            db.session.commit()

        for ramo in catalogo.ramos:
            course = Course.query.filter_by(code=ramo.codigo).first()
            if course:
                continue

            course = Course(
                name=ramo.nombre,
                code=ramo.codigo,
                sct=ramo.sct,
                department=department.id,
                requisitos=ramo.requisitos,
            )
            db.session.add(course)

            db.session.commit()
