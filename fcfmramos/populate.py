import asyncio
from flask_sqlalchemy import SQLAlchemy

from fcfmramos.web_scraper.main import main
from fcfmramos.model.course import Departamento, Ramo, Curso, Profesor


def populate(db: SQLAlchemy):
    catalogos = asyncio.run(main())

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
                        cupos_ocupados=curso.cupos_ocupados
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

        db.session.commit()
