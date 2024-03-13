from flask import Flask
from flask import session

from fcfmramos import secrets


def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.secret_key

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI="sqlite:///project.sqlite",
    )

    from fcfmramos.model import db
    from flask_migrate import Migrate

    db.init_app(app)
    Migrate(app, db)

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

    from fcfmramos.view import auth, main, catalog

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(catalog.bp)

    @app.cli.command("catalogos_scraper")
    def catalogos_scraper():
        from fcfmramos.populate import populate_catalogos

        with app.app_context():
            populate_catalogos(db)

    @app.cli.command("planes_scraper")
    def planes_scraper():
        from fcfmramos.populate import populate_planes

        with app.app_context():
            populate_planes(db)

    return app
