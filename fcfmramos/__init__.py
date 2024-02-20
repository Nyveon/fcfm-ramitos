import asyncio

from flask import Flask
from flask import session

from fcfmramos import config


def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI="sqlite:///project.sqlite",
    )

    from fcfmramos.model import db

    db.init_app(app)

    @app.cli.command()
    def createdb():
        with app.app_context():
            print("Trying to create tables")
            db.create_all()

    @app.context_processor
    def inject_logged_in():
        return dict(is_logged_in=auth.is_logged_in())

    @app.context_processor
    def inject_username():
        return dict(username=session.get("username", ""))

    @app.context_processor
    def inject_verified():
        return dict(is_verified=auth.is_verified())

    from fcfmramos.view import auth, main

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    @app.cli.command()
    def runscraper():
        from fcfmramos.web_scraper.main import main
        from fcfmramos.model.course import Course, Department

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

        print(catalogo)

    return app
